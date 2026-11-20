from django.conf import settings
from django.db import DatabaseError
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from wagtail import __version__ as wagtail_version

from reference.editorial import published_article
from reference.models import ReferencePage
from reference.preview import preview


@never_cache
@require_GET
def diagnostic(request, operation):
    identity = {"site_id": settings.STUDIO_SITE_ID, "instance_id": settings.ENGINE_INSTANCE_ID}
    if operation == "identity":
        return JsonResponse({**identity, "contract_major": 1})
    if operation == "version":
        capabilities = ["editorial.published.v1"] if settings.EDITORIAL_WAGTAIL_SITE_ID else []
        if settings.ENGINE_PREVIEW_ENABLED:
            capabilities.append("preview.v1")
        return JsonResponse({**identity, "contract_major": 1, "contract_minor": 0, "engine_version": "1.0.0",
                             **({"capabilities": capabilities} if capabilities else {}),
                             "wagtail_version": wagtail_version, "image_digest": settings.ENGINE_IMAGE_DIGEST})
    try:
        page = ReferencePage.objects.select_related("live_revision").live().get(**identity)
        if page.live_revision_id is None:
            raise ReferencePage.DoesNotExist
        if operation == "render":
            response = page.live_revision.as_object().serve(request)
            response["X-Studio-Site"] = identity["site_id"]
            response["X-Studio-Instance"] = identity["instance_id"]
            return response
    except (ReferencePage.DoesNotExist, ReferencePage.MultipleObjectsReturned, DatabaseError):
        return JsonResponse({**identity, "status": "unavailable"}, status=503)
    return JsonResponse({**identity, "status": "ready"})


urlpatterns = [path(f"internal/{name}", diagnostic, {"operation": name})
               for name in ("identity", "version", "health", "render")]

urlpatterns.append(path("internal/editorial/v1/article/<int:page_id>", published_article))

urlpatterns.append(path("internal/preview/v1/render", preview))
