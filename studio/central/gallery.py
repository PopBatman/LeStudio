from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_safe
from django.views.static import serve


@require_safe
def gallery(request, asset=None):
    if not settings.STUDIO_UI_GALLERY:
        raise Http404
    if asset is not None:
        return serve(request, asset, document_root=settings.BASE_DIR / "static" / "ui")
    return render(request, "ui/gallery.html")
