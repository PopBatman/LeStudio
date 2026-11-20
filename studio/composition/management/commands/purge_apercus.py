from django.core.management.base import BaseCommand
from django.utils import timezone

from composition.models import PreviewTicket


class Command(BaseCommand):
    help = "Supprime les reçus d’aperçu arrivés à échéance."

    def handle(self, *args, **options):
        count, _ = PreviewTicket.objects.filter(expires_at__lte=timezone.now()).delete()
        self.stdout.write(f"Reçus d’aperçu échus supprimés : {count}.")
