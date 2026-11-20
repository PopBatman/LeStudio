from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.debug import sensitive_variables

from registre import services as registry
from registre.views import require_manager, screen

from . import services


@screen("GET", "HEAD")
def history(request, pk):
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    manage = registry.can_manage(request.user, site)
    try:
        rows, cursor = services.submissions(request.user, pk, request.GET.get("cursor"))
    except ValidationError:
        return render(request, "depots/staff_cursor_error.html", {"site": site}, status=400)
    invitations = Paginator(services.invitations(request.user, pk), 20)
    return render(request, "depots/staff_history.html", {
        "site": site,
        "manage": manage,
        "invitations": invitations.get_page(request.GET.get("invitations", 1)),
        "submissions": rows,
        "next_cursor": cursor,
    })


@screen("POST")
@sensitive_variables("code", "share_url")
def issue(request, pk):
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    invitation, code = services.create_invitation(request.user, pk)
    share_url = settings.STUDIO_PORTAL_ORIGIN.rstrip("/") + "/depot/#" + code
    response = render(request, "depots/staff_issued.html", {
        "site": site, "invitation": invitation, "code": code, "share_url": share_url,
    })
    response["Referrer-Policy"] = "same-origin"
    return response


@screen("GET", "HEAD", "POST")
def revoke(request, pk, invitation_id):
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    require_manager(request.user, site)
    if request.method == "POST":
        services.revoke_invitation(request.user, pk, invitation_id)
        return redirect(reverse("registre:site-depots", args=[pk]) + "?resultat=revoquee")
    invitation = get_object_or_404(services.invitations(request.user, pk), pk=invitation_id)
    return render(request, "depots/staff_revoke.html", {"site": site, "invitation": invitation})


@screen("GET", "HEAD")
def submission(request, pk, submission_id):
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    row = services.submission_for(request.user, pk, submission_id)
    return render(request, "depots/staff_submission.html", {
        "site": site, "row": row, "manage": registry.can_manage(request.user, site),
    })


@screen("GET", "HEAD", "POST")
def erase(request, pk, submission_id):
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    require_manager(request.user, site)
    if request.method == "POST":
        services.erase_submission(request.user, pk, submission_id)
        return redirect(reverse("registre:site-depots", args=[pk]) + "?resultat=efface")
    row = services.submission_for(request.user, pk, submission_id)
    return render(request, "depots/staff_erase.html", {"site": site, "row": row})
