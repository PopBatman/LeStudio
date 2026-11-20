from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.management.base import BaseCommand, CommandError
from django.http import Http404

from depots.services import erase_submission, purge


class Command(BaseCommand):
    help = "Purge les données échues ou efface une remise pour un gestionnaire de site."

    def add_arguments(self, parser):
        parser.add_argument("--operateur")
        parser.add_argument("--site")
        parser.add_argument("--soumission")

    def handle(self, *args, **options):
        action = [options[name] for name in ("operateur", "site", "soumission")]
        if any(value is not None for value in action):
            if not all(action):
                raise CommandError("L’effacement ciblé requiert --operateur, --site et --soumission.")
            actor = get_user_model().objects.filter(username=action[0], is_active=True).first()
            if actor is None:
                raise CommandError("Opération indisponible.")
            try:
                erase_submission(actor, action[1], action[2])
            except (Http404, PermissionDenied):
                raise CommandError("Opération indisponible.") from None
            self.stdout.write("Effacement de la remise effectué.")
            return
        count = purge()
        self.stdout.write(f"Remises arrivées à échéance et effacées : {count}.")
