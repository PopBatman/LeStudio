from django.urls import path

from . import public

app_name = "depot_public"
urlpatterns = [
    path("", public.entry, name="entry"),
    path("version/", public.deposit, name="deposit"),
    path("recu/<uuid:submission_id>/", public.receipt, name="receipt"),
]
