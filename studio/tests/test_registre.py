from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch

from django.contrib.auth.models import Group, Permission, User
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, connections, transaction
from django.http import Http404
from django.test import TestCase, TransactionTestCase, skipUnlessDBFeature

from registre import services as api
from registre.models import Client, Contact, ClientGrant, SiteGrant
from workspace.access import OPERATOR_GROUP


class RegistryTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner")
        self.worker = User.objects.create_user("worker", is_superuser=True)
        group = Group.objects.create(name=OPERATOR_GROUP)
        group.user_set.add(self.owner, self.worker)
        self.owner.user_permissions.add(
            Permission.objects.get(content_type__app_label="registre", codename="create_client")
        )
        self.client_obj = api.create_client(
            self.owner, {"display_name": " Atelier ", "client_type": "COMPANY"}
        )
        self.site = api.create_site(self.owner, self.client_obj.pk, {"name": "Vitrine"})
        self.other = api.create_site(self.owner, self.client_obj.pk, {"name": "Catalogue"})

    def test_independent_scopes_and_revocation(self):
        self.assertFalse(api.can_create_client(self.worker))
        grant = SiteGrant.objects.create(user=self.worker, site=self.site, level="read")
        self.assertFalse(api.clients(self.worker).exists())
        self.assertEqual(list(api.sites(self.worker)), [self.site])
        with self.assertRaises(PermissionDenied):
            api.update_site(self.worker, self.site.pk, {"name": "X"}, self.site.updated_at)
        with self.assertRaises(Http404):
            api.update_site(self.worker, self.other.pk, {"name": "X"}, self.other.updated_at)
        grant.delete()
        self.assertFalse(api.sites(self.worker).exists())

    def test_archive_version_and_domain(self):
        c = self.client_obj
        active = api.archive_client(self.owner, c.pk, True, c.updated_at)
        self.assertEqual(
            api.archive_client(self.owner, c.pk, True, c.updated_at).archived_at, active.archived_at
        )
        with self.assertRaises(api.Conflict):
            api.create_site(self.owner, c.pk, {"name": "Nouveau"})
        edited = api.update_site(
            self.owner, self.site.pk, {"domain": "ÉCOLE.example."}, self.site.updated_at
        )
        self.assertEqual(edited.domain, "xn--cole-9oa.example")
        with self.assertRaises(api.Conflict):
            api.update_site(self.owner, self.site.pk, {"name": "Périmé"}, self.site.updated_at)
        self.assertIsNone(
            api.archive_client(self.owner, c.pk, False, active.updated_at).archived_at
        )

    def test_contacts_normalization_and_parent(self):
        c = self.client_obj
        data = {"display_name": "A", "role": "Technique", "phone": "06 (23) 45-67.89"}
        contact = api.save_contact(self.owner, c.pk, data)
        self.assertEqual(contact.phone, "0623456789")
        with self.assertRaises(ValidationError):
            api.save_contact(self.owner, c.pk, {"phone": " "}, contact.pk, contact.updated_at)
        updated = api.save_contact(
            self.owner,
            c.pk,
            {"phone": "", "email": " A@EXAMPLE.ORG "},
            contact.pk,
            contact.updated_at,
        )
        self.assertEqual(updated.email, "A@example.org")
        another = api.create_client(
            self.owner, {"display_name": "Atelier", "client_type": "INDIVIDUAL"}
        )
        with self.assertRaises(Http404):
            api.save_contact(self.owner, another.pk, data, contact.pk, updated.updated_at)
        with self.assertRaises(ValidationError):
            api.update_site(
                self.owner, self.site.pk, {"client_id": another.pk}, self.site.updated_at
            )

    def test_services_reject_null_bytes_before_validation_queries(self):
        version = self.client_obj.updated_at
        with self.assertRaises(ValidationError) as rejected:
            api.update_client(self.owner, self.client_obj.pk, {"display_name": "A\x00B"}, version)
        self.assertIn("display_name", rejected.exception.message_dict)
        self.client_obj.refresh_from_db()
        self.assertEqual(self.client_obj.updated_at, version)

    def test_rollback_and_database_invariants(self):
        with patch.object(ClientGrant.objects, "create", side_effect=IntegrityError):
            with self.assertRaises(IntegrityError):
                api.create_client(
                    self.owner, {"client_type": "ASSOCIATION", "display_name": "Autre"}
                )
        self.assertEqual(Client.objects.count(), 1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Contact.objects.create(client=self.client_obj, display_name="A", role="T", phone="  ")


@skipUnlessDBFeature("has_select_for_update")
class ConcurrentRegistryTests(TransactionTestCase):
    def test_two_concurrent_edits_preserve_first_successful_write(self):
        operator = User.objects.create_user("editor")
        Group.objects.create(name=OPERATOR_GROUP).user_set.add(operator)
        client = Client.objects.create(display_name="Nom initial", client_type="ASSOCIATION")
        ClientGrant.objects.create(client=client, user=operator, level="manage")
        original_version = client.updated_at
        ready = Barrier(2)

        def edit(name):
            try:
                actor = User.objects.get(pk=operator.pk)
                ready.wait(timeout=8)
                try:
                    api.update_client(actor, client.pk, {"display_name": name}, original_version)
                except api.Conflict:
                    return None
                return name
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(edit, ["Première édition", "Seconde édition"]))
        client.refresh_from_db()
        self.assertCountEqual(results, [None, client.display_name])
