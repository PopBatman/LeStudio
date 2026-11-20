from io import StringIO
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command, CommandError
from django.test import TestCase

from workspace.access import OPERATOR_GROUP


class RegistryAccessCommandTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("operatrice")
        self.user.groups.add(Group.objects.create(name=OPERATOR_GROUP))

    def run_command(self, *args):
        call_command("registre_access", *map(str, args), stdout=StringIO())

    def test_nominal_creation_permission_round_trip(self):
        permissions = self.user.user_permissions.filter(
            content_type__app_label="registre", codename="create_client"
        )
        for _ in range(2):
            self.run_command("grant", self.user.username, "create-client")
            self.assertTrue(permissions.exists())
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
        for _ in range(2):
            self.run_command("revoke", self.user.username, "create-client")
            self.assertFalse(permissions.exists())

    def test_grants_only_the_requested_object_and_supports_downgrade(self):
        from registre.models import Client, ClientGrant, Site, SiteGrant

        client = Client.objects.create(display_name="Atelier", client_type="COMPANY")
        site = Site.objects.create(client=client, name="Atelier en ligne")
        sibling = Site.objects.create(client=client, name="Catalogue")
        for level in ("manage", "manage", "read"):
            self.run_command("grant", self.user.username, "site", site.pk, "--level", level)
            grant = SiteGrant.objects.get(user=self.user)
            self.assertEqual((grant.site_id, grant.level), (site.pk, level))
            self.assertFalse(ClientGrant.objects.filter(user=self.user).exists())
        self.run_command("grant", self.user.username, "client", client.pk, "--level", "manage")
        self.run_command("revoke", self.user.username, "site", site.pk)
        self.run_command("revoke", self.user.username, "site", sibling.pk)
        self.assertFalse(SiteGrant.objects.filter(user=self.user).exists())
        self.assertTrue(ClientGrant.objects.filter(user=self.user, client=client, level="manage").exists())

    def test_unknown_target_or_invalid_arguments_do_not_grant_access(self):
        for args in (
            ("grant", "inconnu", "create-client"),
            ("grant", self.user.username, "client", uuid4(), "--level", "read"),
            ("grant", self.user.username, "site", "incorrect", "--level", "read"),
            ("grant", self.user.username, "site", uuid4()),
            ("grant", self.user.username, "create-client", "--level", "manage"),
            ("revoke", self.user.username, "create-client", uuid4()),
        ):
            with self.subTest(args=args), self.assertRaises(CommandError):
                self.run_command(*args)
        self.assertFalse(self.user.user_permissions.exists())

    def test_grant_requires_an_active_operator(self):
        self.user.groups.clear()
        with self.assertRaises(CommandError):
            self.run_command("grant", self.user.username, "create-client")
        self.assertFalse(self.user.user_permissions.exists())
