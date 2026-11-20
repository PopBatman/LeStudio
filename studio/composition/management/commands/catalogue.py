from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from composition.catalogue import DEMO_RIGHTS, PARAMETERS, attribuer_media, installer_version
from composition.models import ComponentVersion
from registre.models import Site


class Command(BaseCommand):
    help = "Livrer les versions codées et attribuer le visuel de démonstration depuis le poste technique."

    def add_arguments(self, parser):
        commands = parser.add_subparsers(dest="action", required=True)
        media = commands.add_parser("media", help="Attribuer ou révoquer le média de démonstration.")
        media.add_argument("site", metavar="UUID_SITE")
        media.add_argument("decision", choices=["attribuer", "revoquer"])
        install = commands.add_parser("version", help="Installer une version de composant déjà développée.")
        install.add_argument("site", metavar="UUID_SITE_OU_global")
        install.add_argument("key")
        install.add_argument("version", type=int)
        install.add_argument("renderer", choices=PARAMETERS)
        install.add_argument("label")
        retire = commands.add_parser("retirer", help="Retirer une version de la sélection des nouvelles occurrences.")
        retire.add_argument("site", metavar="UUID_SITE_OU_global")
        retire.add_argument("key")
        retire.add_argument("version", type=int)

    def handle(self, *args, **options):
        try:
            site = None if options["site"] == "global" else Site.objects.get(pk=options["site"])
            if options["action"] == "media":
                if site is None:
                    raise CommandError("L’attribution du média exige un site.")
                row = attribuer_media(site, actif=options["decision"] == "attribuer")
                return f"{row.pk} · {options['decision']} · {DEMO_RIGHTS}"
            if options["action"] == "retirer":
                changed = ComponentVersion.objects.filter(
                    site=site, key=options["key"], version=options["version"]).update(retired=True)
                if not changed:
                    raise CommandError("Version absente du catalogue de cette portée.")
                return "Version retirée des nouvelles sélections."
            row = installer_version(site, options["key"], options["version"], options["label"], options["renderer"])
            return f"{row.key} v{row.version} · {row.pk}"
        except (ValidationError, Site.DoesNotExist) as exc:
            raise CommandError(f"Attribution ou livraison refusée. {exc}") from None
