import json
from uuid import UUID

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from raccordement.services import inspect_link, LinkError, verify_link


class Command(BaseCommand):
    help = "Vérifier ou consulter une liaison au moteur sous le mandat explicite d’un opérateur."

    def add_arguments(self, parser):
        parser.add_argument("action", choices=["verifier", "etat"])
        parser.add_argument("acteur")
        parser.add_argument("site", type=UUID)
        parser.add_argument("profil", nargs="?")

    def handle(self, *, action, acteur, site, profil, **options):
        if (action == "verifier") != bool(profil):
            raise CommandError("Indiquer le profil uniquement pour la vérification.")
        user = get_user_model().objects.filter(username=acteur).first()
        if user is None:
            raise CommandError("not_found")
        try:
            result = verify_link(user, site, profil) if profil else inspect_link(user, site)
        except LinkError as error:
            raise CommandError(str(error)) from None
        return json.dumps(result, ensure_ascii=False)
