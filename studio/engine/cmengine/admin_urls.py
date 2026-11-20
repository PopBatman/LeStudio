from django.urls import include, path
from wagtail.admin import urls as admin_urls
from wagtail.documents import urls as document_urls
from wagtail import urls as wagtail_urls

urlpatterns = [
    path("admin/", include(admin_urls)),
    path("documents/", include(document_urls)),
    path("pages/", include(wagtail_urls)),
]
