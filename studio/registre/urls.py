from django.urls import path

from composition import builder_views, preview_views
from composition.catalogue_views import library, media
from composition.editor_navigation import legacy
from composition.editorial_views import articles
from composition.views import navigation
from depots import comparison_views, import_views, staff as deposit_staff

from . import views

app_name = "registre"
urlpatterns = [
    path("clients/", views.client_list, name="clients"),
    path("clients/nouveau/", views.client_form, name="client-new"),
    path("clients/<uuid:pk>/", views.client_detail, name="client"),
    path("clients/<uuid:pk>/modifier/", views.client_form, name="client-edit"),
    path("clients/<uuid:pk>/archiver/", views.archive, {"archived": True}, name="archive"),
    path("clients/<uuid:pk>/reactiver/", views.archive, {"archived": False}, name="restore"),
    path("clients/<uuid:pk>/contacts/nouveau/", views.contact_form, name="contact-new"),
    path("clients/<uuid:pk>/contacts/<uuid:child>/modifier/", views.contact_form, name="contact-edit"),
    path("clients/<uuid:pk>/sites/nouveau/", views.site_create, name="site-new"),
    path("sites/", views.site_list, name="sites"),
    path("sites/<uuid:pk>/", views.site_detail, name="site"),
    path("sites/<uuid:pk>/apercu/", preview_views.prepare, name="preview"),
    path("sites/<uuid:pk>/apercu/<uuid:ticket>/", preview_views.view, name="preview-view"),
    path("sites/<uuid:pk>/apercu/<uuid:ticket>/document/", preview_views.document, name="preview-document"),
    path("sites/<uuid:pk>/apercu/<uuid:ticket>/fermer/", preview_views.close, name="preview-close"),
    path("sites/<uuid:pk>/depots/", deposit_staff.history, name="site-depots"),
    path("sites/<uuid:pk>/depots/invitations/creer/", deposit_staff.issue, name="depot-invite"),
    path("sites/<uuid:pk>/depots/invitations/<uuid:invitation_id>/revoquer/", deposit_staff.revoke, name="depot-revoke"),
    path("sites/<uuid:pk>/depots/soumissions/<uuid:submission_id>/", deposit_staff.submission, name="depot-submission"),
    path("sites/<uuid:pk>/depots/soumissions/<uuid:submission_id>/import/", import_views.review, name="depot-import"),
    path("sites/<uuid:pk>/depots/soumissions/<uuid:submission_id>/effacer/", deposit_staff.erase, name="depot-erase"),
    path("sites/<uuid:pk>/atelier/visuel/figma/<uuid:revision_id>/<uuid:page_id>/", comparison_views.compare, name="figma-compare"),
    path("sites/<uuid:pk>/atelier/visuel/references/<uuid:reference_id>/", comparison_views.image, name="figma-reference"),
    path("sites/<uuid:pk>/atelier/visuel/", builder_views.prepare, name="site-builder"),
    path("sites/<uuid:pk>/atelier/visuel/enregistrer/", builder_views.save, name="builder-save"),
    path("sites/<uuid:pk>/atelier/visuel/<uuid:ticket>/", builder_views.view, name="builder-view"),
    path("sites/<uuid:pk>/atelier/visuel/<uuid:ticket>/document/", builder_views.document, name="builder-document"),
    path("sites/<uuid:pk>/atelier/articles/", articles, name="site-articles"),
    path("sites/<uuid:pk>/atelier/canvas/", legacy, {"canvas": True}, name="site-canvas"),
    path("sites/<uuid:pk>/atelier/", legacy, name="site-editor"),
    path("sites/<uuid:pk>/bibliotheque/", library, {"tab": "catalogue"}, name="site-catalogue"),
    path("sites/<uuid:pk>/apparence/", library, {"tab": "appearance"}, name="site-appearance"),
    path("sites/<uuid:pk>/bibliotheque/medias/<uuid:asset>/", media, name="site-media"),
    path("sites/<uuid:pk>/pages/", navigation, {"tab": "pages"}, name="site-pages"),
    path("sites/<uuid:pk>/menus/", navigation, {"tab": "menus"}, name="site-menus"),
    path("sites/<uuid:pk>/modifier/", views.site_edit, name="site-edit"),
]
