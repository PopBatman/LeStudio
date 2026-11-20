from importlib import import_module
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.apps import apps
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import connection
from django.utils import timezone

from composition.editor import creer_atelier, modifier_structure
from composition.editorial import SourceChanged, confirmer_article, lire_article, verifier_article
from composition.models import ComponentVersion, EditorialReference, CompositionRevision
from raccordement.models import SiteConnection
from registre.models import Client, Site, SiteGrant
from registre.services import Conflict
from tests.catalogue_fixture import CatalogueTestCase
from workspace.access import OPERATOR_GROUP


class EditorialServicesTests(CatalogueTestCase):
    def setUp(self):
        self.actor = User.objects.create_user("Gestion")
        self.actor.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        client = Client.objects.create(client_type="COMPANY", display_name="Exemple")
        self.site = Site.objects.create(client=client, name="Atelier")
        self.grant = SiteGrant.objects.create(site=self.site, user=self.actor, level="manage")
        self.profile = SimpleNamespace(engine_version="1.1", image_digest="digest", instance_id=uuid4(), site_id=self.site.pk)
        now = timezone.now()
        self.link = SiteConnection.objects.create(site=self.site, instance_id=self.profile.instance_id,
            confirmed_profile="demo", confirmed_at=now, started_at=now, finished_at=now, expires_at=now,
            attempt_id=uuid4(), diagnostic="connected", versions={"engine_version":"1.1","image_digest":"digest","capabilities": ["editorial.published.v1"]})
        self.head = creer_atelier(self.actor, self.site.pk, "template")
        self.page = self.head["document"]["pages"][0]
        self.parent = self.page["sections"][0]["id"]
        profile = patch("composition.editorial.load_profile", return_value=self.profile)
        profile.start()
        self.addCleanup(profile.stop)
        reader = patch("composition.editorial.read_published_article", return_value="101")
        self.reader = reader.start()
        self.addCleanup(reader.stop)

    def verify(self):
        return verifier_article(self.actor, self.site.pk, 42)

    def confirm(self, obs, **kw):
        return confirmer_article(self.actor, self.site.pk, self.head["id"], obs["token"],
                                 page=self.page["id"], **kw)

    def test_preexisting_promoted_article_keeps_its_pinned_version(self):
        # Recreate a catalogue where a shared text component claimed the name before 0004.
        from composition.catalogue_v1 import manifest

        ComponentVersion.objects.filter(site=None, key="article").update(
            origin="promotion_revue", renderer="text", manifest=manifest("text"))
        migration = import_module("composition.migrations.0004_editorial")
        migration.seed_article(apps, SimpleNamespace(connection=connection))
        migration.seed_article(apps, SimpleNamespace(connection=connection))
        versions = ComponentVersion.objects.filter(site=None, key="article").order_by("version")
        self.assertEqual(list(versions.values_list("version", "renderer")), [(1, "text"), (2, "article")])
        envelope, node = self.confirm(self.verify(), parent=self.parent)
        blocks = envelope["document"]["pages"][0]["sections"][0]["blocks"]
        self.assertEqual(next(b for b in blocks if b["id"] == str(node))["definition"]["version"], 2)

    def test_changed_publication_and_immutable_history(self):
        first = self.verify()
        self.reader.return_value = "102"
        with self.assertRaises(SourceChanged) as changed:
            self.confirm(first, parent=self.parent)
        self.assertEqual(EditorialReference.objects.count(), 0)
        self.head, node = self.confirm(changed.exception.observation, parent=self.parent)
        block = self.head["document"]["pages"][0]["sections"][0]["blocks"][-1]
        ref = block["props"]["content"]["ref_id"]
        self.assertEqual(lire_article(self.actor, self.site.pk, ref)["status"], "concordant")
        self.reader.return_value = "103"
        next_obs = self.verify()
        self.assertEqual(lire_article(self.actor, self.site.pk, ref)["status"], "divergent")
        self.head, same = self.confirm(next_obs, node=node)
        self.assertEqual(same, node)
        self.assertEqual(EditorialReference.objects.count(), 2)
        with self.assertRaises(ValidationError):
            modifier_structure(self.actor, self.site.pk, self.head["id"], {"action":"block_add",
                "page":self.page["id"], "parent":self.parent, "definition":block["definition"], "props":block["props"]})

    def test_permissions_capability_and_late_result(self):
        self.link.versions = {}
        self.link.save()
        self.assertEqual(self.verify()["status"], "unavailable")
        self.reader.assert_not_called()
        self.link.versions = {"engine_version":"1.1","image_digest":"digest","capabilities": ["editorial.published.v1"]}
        self.link.save()
        def late(*args):
            self.reader.side_effect = None
            self.verify()
            return "100"
        self.reader.side_effect = late
        with self.assertRaises(Conflict):
            self.verify()
        def revoke(*args):
            SiteGrant.objects.filter(pk=self.grant.pk).update(level="read")
            return "101"
        self.reader.side_effect = revoke
        with self.assertRaises(PermissionDenied):
            self.verify()
        self.assertEqual(CompositionRevision.objects.count(), 1)

    def test_isolation_last_success_and_independent_edit(self):
        from django.http import Http404
        from composition.editorial import lire_observation
        from raccordement.transport import ProbeError
        self.head, node = self.confirm(self.verify(), parent=self.parent)
        block = self.head["document"]["pages"][0]["sections"][0]["blocks"][-1]
        pin = block["props"]["content"]["ref_id"]
        other = Site.objects.create(client=self.site.client, name="Autre site")
        SiteGrant.objects.create(user=self.actor, site=other, level="manage")
        self.assertIsNone(lire_article(self.actor, other.pk, pin)["page_number"])
        with self.assertRaises(Http404):
            lire_observation(self.actor, other.pk, lire_article(self.actor, self.site.pk, pin)["observation"]["token"])
        self.reader.side_effect = ProbeError("inaccessible")
        self.verify()
        state = lire_article(self.actor, self.site.pk, pin)
        self.assertEqual(state["status"], "inaccessible")
        self.assertIsNone(state["observation"]["published_revision"])
        self.assertIsNotNone(state["observation"]["last_success_at"])
        self.head, _ = modifier_structure(self.actor, self.site.pk, self.head["id"],
                                          {"action":"section_add", "page": self.page["id"]})
        self.assertEqual(self.head["document"]["pages"][0]["sections"][0]["blocks"][-1], block)
        with self.assertRaises(ValidationError):
            EditorialReference.objects.filter(pk=pin).delete()
        with self.assertRaises(ValidationError):
            EditorialReference.objects.filter(pk=pin).update(published_revision="9")

    def test_invalid_input_unchanged_confirmation_and_tampered_profile(self):
        for number in (True, -1, 0, "42", 2147483648):
            with self.subTest(number=number), self.assertRaises(ValidationError):
                verifier_article(self.actor, self.site.pk, number)
        self.reader.assert_not_called()
        self.head, node = self.confirm(self.verify(), parent=self.parent)
        unchanged, _ = self.confirm(self.verify(), node=node)
        self.assertEqual(unchanged["id"], self.head["id"])
        def change_identity(*args):
            SiteConnection.objects.filter(site=self.site).update(instance_id=uuid4())
            return "900"
        self.reader.side_effect = change_identity
        self.assertEqual(self.verify()["status"], "unavailable")
        self.assertEqual(EditorialReference.objects.count(), 1)

    def test_replaced_profile_requires_new_qualification(self):
        self.head, _ = self.confirm(self.verify(), parent=self.parent)
        pin = EditorialReference.objects.get()
        self.profile.image_digest = "different"
        self.reader.reset_mock()
        self.assertEqual(lire_article(self.actor, self.site.pk, pin.pk)["status"], "unavailable")
        self.assertEqual(self.verify()["status"], "unavailable")
        self.reader.assert_not_called()

    def test_two_instances_can_have_same_native_ids_and_private_copy_is_scoped(self):
        from composition.services import ScopedComposition, creer_brouillon
        first_head, _ = self.confirm(self.verify(), parent=self.parent)
        original_site = self.site
        first_pin = EditorialReference.objects.get()
        other = Site.objects.create(client=self.site.client, name="B")
        SiteGrant.objects.create(site=other, user=self.actor, level="manage")
        origin = {"kind": "template", "ref": "guide", "version": "1"}
        for version in (3, 4):
            document = {**first_head["document"], "schema_version": version}
            with self.subTest(version=version), self.assertRaises(ValidationError):
                creer_brouillon(self.actor, other.pk, origin,
                    resolve_origin=lambda *args: ScopedComposition(original_site.pk, document))
        self.site = other
        self.profile = SimpleNamespace(site_id=other.pk, instance_id=uuid4(),
                                       engine_version="1.1", image_digest="digest")
        self.link.site = other
        self.link.instance_id = self.profile.instance_id
        self.link.attempt_id = uuid4()
        self.link.save(force_insert=True)
        self.head = creer_atelier(self.actor, other.pk, "template")
        self.page = self.head["document"]["pages"][0]
        with patch("composition.editorial.load_profile", return_value=self.profile):
            second_head, _ = self.confirm(self.verify(), parent=self.page["sections"][0]["id"])
        second_pin = EditorialReference.objects.get(site=other)
        self.assertNotEqual(first_pin.pk, second_pin.pk)
        self.assertEqual(first_pin.page_number, second_pin.page_number)
        self.assertEqual(first_pin.published_revision, second_pin.published_revision)
        self.assertNotIn(str(first_pin.pk), str(second_head["document"]))
