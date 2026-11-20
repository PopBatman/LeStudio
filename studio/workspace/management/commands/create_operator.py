from getpass import getpass, GetPassWarning
import warnings

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction

from workspace.access import OPERATOR_GROUP


class Command(BaseCommand):
    help = "Créer un compte opérateur local et saisir son mot de passe au terminal."

    def add_arguments(self, parser):
        parser.add_argument("username", metavar="IDENTIFIANT")

    def handle(self, *args, **options):
        User = get_user_model()
        user = User(username=User.normalize_username(options["username"]))
        try:
            user.full_clean(exclude=["password"])
        except ValidationError as error:
            raise CommandError(" ".join(error.messages)) from error

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", GetPassWarning)
                password = getpass("Mot de passe : ")
                confirmation = getpass("Confirmer le mot de passe : ")
        except (GetPassWarning, EOFError, KeyboardInterrupt) as error:
            raise CommandError("Création interrompue. Utilisez un terminal avec saisie masquée.") from error

        if password != confirmation:
            raise CommandError("Les deux mots de passe diffèrent.")
        if not password.strip():
            raise CommandError("Le mot de passe est vide.")
        try:
            validate_password(password, user)
        except ValidationError as error:
            raise CommandError(" ".join(error.messages)) from error

        user.set_password(password)
        try:
            with transaction.atomic():
                user.save(force_insert=True)
                group, _ = Group.objects.get_or_create(name=OPERATOR_GROUP)
                user.groups.add(group)
        except IntegrityError as error:
            raise CommandError("Impossible de créer ce nouvel opérateur.") from error

        self.stdout.write(self.style.SUCCESS(f"Compte opérateur créé pour {user.username}."))
