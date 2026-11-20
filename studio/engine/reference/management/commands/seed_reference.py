from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wagtail.models import Page, Site

from reference.models import ReferencePage


class Command(BaseCommand):
    help = "Initialise la page Wagtail de référence d’une instance de qualification."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        root = Page.objects.select_for_update().get(depth=1)
        if page := ReferencePage.objects.first():
            if (str(page.site_id), str(page.instance_id)) != (settings.STUDIO_SITE_ID, settings.ENGINE_INSTANCE_ID):
                raise CommandError("Identité incompatible avec la base de cette instance.")
            return
        page = ReferencePage(title="Référence Studio", slug="reference-studio", marker=settings.ENGINE_MARKER,
                             site_id=settings.STUDIO_SITE_ID, instance_id=settings.ENGINE_INSTANCE_ID)
        root.add_child(instance=page)
        page.save_revision().publish()
        Site.objects.update_or_create(is_default_site=True, defaults={"hostname":"localhost", "root_page":page})
