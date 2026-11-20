from django.conf import settings
from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.urls import include, path, re_path
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_safe
from django.views.static import serve

from workspace.views import OperatorLoginView, sign_out, workspace

from .gallery import gallery


@csrf_exempt
@require_safe
@never_cache
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse({"status": "unavailable"}, status=503)
    return JsonResponse({"status": "ok"})


# Both development endpoints reject writes with 405 before processing any input.
gallery_read_only = csrf_exempt(gallery)

urlpatterns = [
    path("", workspace, name="workspace"),
    path("", include("registre.urls")),
    path("depot/", include("depots.public_urls")),
    path("connexion/", OperatorLoginView.as_view(), name="login"),
    path("deconnexion/", sign_out, name="logout"),
    re_path(
        r"^assets/(?P<path>gallery\.css|workspace\.css|registre\.css|(?:preview|builder|builder-edit|figma-compare)\.(?:js|css)|builder-(?:drop|edit-model)\.js|editor\.js|canvas\.js|canvas\.css|depot-public\.(?:css|js)|depot-staff\.js|fonts/dm-sans-latin\.woff2)$",
        require_safe(serve),
        {"document_root": settings.BASE_DIR / "static" / "ui"},
    ),
    path("health/", health),
    path("ui/", gallery_read_only, name="ui-gallery"),
    re_path(r"^ui/assets/(?P<asset>gallery\.css|gallery\.js|fonts/dm-sans-latin\.woff2)$", gallery_read_only),
]
