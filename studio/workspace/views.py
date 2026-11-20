from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST, require_safe

from .access import is_operator


class OperatorAuthenticationForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        "invalid_login": "Identifiant ou mot de passe incorrect, ou accès non autorisé.",
    }

    def confirm_login_allowed(self, user):
        if not is_operator(user):
            raise self.get_invalid_login_error()


class OperatorLoginView(LoginView):
    template_name = "workspace/login.html"
    authentication_form = OperatorAuthenticationForm
    redirect_authenticated_user = True
    http_method_names = ["get", "head", "post", "options"]

    def get_success_url(self):
        return reverse("workspace")


@never_cache
@require_safe
@login_required
def workspace(request):
    if not is_operator(request.user):
        return render(request, "workspace/forbidden.html", status=403)
    return render(request, "workspace/home.html")


@never_cache
@require_POST
def sign_out(request):
    logout(request)
    return redirect("login")
