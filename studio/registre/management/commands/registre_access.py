from uuid import UUID

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from registre.models import Client, ClientGrant, Site, SiteGrant
from workspace.access import is_operator


class Command(BaseCommand):
    help = "Attribuer ou retirer une habilitation nominative dans le registre du Studio."

    def add_arguments(self, parser):
        parser.add_argument("action", choices=("grant", "revoke"))
        parser.add_argument("username", metavar="IDENTIFIANT")
        parser.add_argument("scope", choices=("create-client", "client", "site"))
        parser.add_argument("object_id", nargs="?", metavar="UUID")
        parser.add_argument("--level", choices=("read", "manage"))

    @transaction.atomic
    def handle(self, *, action, username, scope, object_id, level, **options):
        User = get_user_model()
        try:
            user = User.objects.select_for_update().get(username=username)
        except User.DoesNotExist:
            raise CommandError("Identifiant opérateur introuvable.") from None
        if action == "grant" and not is_operator(user):
            raise CommandError("L’attribution exige un compte opérateur actif.")
        if scope == "create-client":
            if object_id or level:
                raise CommandError("La capacité create-client s’attribue sans UUID ni niveau.")
            permission = Permission.objects.get(
                content_type__app_label="registre", content_type__model="client", codename="create_client"
            )
            if action == "grant":
                user.user_permissions.add(permission)
            else:
                user.user_permissions.remove(permission)
        else:
            try:
                pk = UUID(object_id or "")
            except ValueError:
                raise CommandError("Indiquez l’UUID du client ou du site.") from None
            if (action == "grant") != bool(level):
                raise CommandError("Indiquez --level lors d’une attribution uniquement.")
            model, grants = (Client, ClientGrant) if scope == "client" else (Site, SiteGrant)
            try:
                target = model.objects.get(pk=pk)
            except model.DoesNotExist:
                raise CommandError("Cible introuvable dans le registre.") from None
            binding = {"user": user, scope: target}
            if action == "grant":
                grants.objects.update_or_create(**binding, defaults={"level": level})
            else:
                grants.objects.filter(**binding).delete()
        self.stdout.write(self.style.SUCCESS("Habilitation prise en compte."))
