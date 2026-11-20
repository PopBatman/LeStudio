from django.conf import settings
from django.db import DatabaseError
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from wagtail.models import Site

from .models import ArticlePage


def scoped_public_article(page_id):
    page = ArticlePage.objects.live().public().exact_type(ArticlePage).filter(
        pk=page_id, live_revision_id__isnull=False
    ).select_related("live_revision").first()
    if page is None:
        return None
    path = page.path
    ancestors = [path[:i] for i in range(ArticlePage.steplen, len(path) + 1, ArticlePage.steplen)]
    roots = list(Site.objects.filter(root_page__path__in=ancestors).order_by(
        "-root_page__depth"
    ).values_list("pk", "root_page__depth")[:2])
    if (not roots or roots[0][0] != settings.EDITORIAL_WAGTAIL_SITE_ID
            or (len(roots) > 1 and roots[0][1] == roots[1][1])):
        return None
    return page


@never_cache
@require_GET
def published_article(request, page_id):
    refused = JsonResponse({"status": "inaccessible"}, status=404)
    if not settings.EDITORIAL_WAGTAIL_SITE_ID or not 0 < page_id <= 2147483647:
        return refused
    try:
        page = scoped_public_article(page_id)
        if page is None:
            return refused
        return JsonResponse({"site_id": settings.STUDIO_SITE_ID, "instance_id": settings.ENGINE_INSTANCE_ID,
                             "type": "article", "page_id": page_id, "published_revision_id": str(page.live_revision_id)})
    except DatabaseError:
        return JsonResponse({"status": "unavailable"}, status=503)
