from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import timedelta
from threading import Barrier
from unittest.mock import Mock, patch
from uuid import uuid4

from django.contrib.auth.models import AnonymousUser, Group, User
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import connections, transaction
from django.db.models.signals import post_save
from django.http import Http404
from django.test import TestCase, TransactionTestCase, skipUnlessDBFeature
from django.utils import timezone

from composition.models import CompositionRevision
from composition.services import (
    creer_brouillon,
    enregistrer_brouillon,
    lire_brouillon,
    lire_revision,
)
from raccordement.models import SiteConnection
from registre.models import Client, ClientGrant, Site, SiteGrant
from registre.services import Conflict
from workspace.access import OPERATOR_GROUP


def sample_document():
    root = str(uuid4())
    blocks = [
        {
            "id": str(uuid4()),
            "definition": {"scope": "global", "key": "text", "version": 1},
            "props": {"text": title},
            "children": [],
        }
        for title in ("Présentation", "Horaires")
    ]
    return {
        "schema_version": 1,
        "pages": [
            {"id": root, "parent_id": None, "slug": "", "title": "Accueil", "sections": [
                {"id": str(uuid4()), "layout": {"base": {"gap": 12}, "mobile": {"gap": 4}},
                 "blocks": blocks},
            ]},
            {"id": str(uuid4()), "parent_id": root, "slug": "ateliers",
             "title": "Ateliers", "sections": []},
        ],
        "menus": [],
        "theme": {},
    }


def occurrence_ids(doc):
    root, child = doc["pages"]
    section = root["sections"][0]
    return {root["id"], child["id"], section["id"], *(b["id"] for b in section["blocks"])}


class DraftServicesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("gestionnaire")
        self.user.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        self.owner = Client.objects.create(display_name="Maison Exemple", client_type="COMPANY")
        self.site = Site.objects.create(client=self.owner, name="Site principal")
        self.other = Site.objects.create(client=self.owner, name="Autre site")
        self.grant = SiteGrant.objects.create(site=self.site, user=self.user, level="manage")

    def blank(self):
        return creer_brouillon(self.user, self.site.pk, {"kind": "blank"})

    def test_read_unconnected_site_does_not_create_a_draft(self):
        self.assertIsNone(lire_brouillon(self.user, self.site.pk))
        self.assertFalse(CompositionRevision.objects.exists())
        self.assertFalse(SiteConnection.objects.exists())

    def test_blank_current_history_and_existing_connection(self):
        now = timezone.now()
        SiteConnection.objects.create(
            site=self.site, instance_id=uuid4(), confirmed_at=now, confirmed_profile="atelier",
            attempt_id=uuid4(), started_at=now, expires_at=now + timedelta(seconds=20),
            finished_at=now, diagnostic="connected", versions={"wagtail_version": "7.4.4"},
        )
        before_connection = SiteConnection.objects.values().get()
        before_sites = list(Site.objects.order_by("pk").values())
        with patch("raccordement.services.probe") as probe, patch("raccordement.services.load_profile") as profile:
            first = self.blank()
            self.assertEqual(first["document"]["pages"][0]["sections"], [])
            self.assertEqual(first["number"], 1)
            self.assertIsNone(first["parent_id"])
            self.assertEqual(first["site_id"], str(self.site.pk))
            self.assertEqual(first["author_id"], self.user.pk)
            self.assertEqual(first["origin"], {"kind": "blank"})
            self.assertFalse(CompositionRevision.objects.filter(site=self.other).exists())
            changed = deepcopy(first["document"])
            changed["pages"][0]["title"] = "Offre locale"
            second = enregistrer_brouillon(self.user, self.site.pk, first["id"], changed)
            self.assertEqual(second["number"], 2)
            self.assertEqual(second["parent_id"], first["id"])
            self.assertNotEqual(second["id"], first["id"])
            self.assertEqual(second["origin"], first["origin"])
            self.assertEqual(second["document"], changed)
            self.assertEqual(lire_revision(self.user, self.site.pk, first["id"]), first)
            self.assertEqual(lire_brouillon(self.user, self.site.pk), second)
        probe.assert_not_called()
        profile.assert_not_called()
        self.assertEqual(SiteConnection.objects.values().get(), before_connection)
        self.assertEqual(list(Site.objects.order_by("pk").values()), before_sites)

    def test_template_and_accepted_figma_are_copied_and_reloaded_identically(self):
        SiteGrant.objects.create(site=self.other, user=self.user, level="manage")
        source = sample_document()
        original = deepcopy(source)
        copies = []
        for site, kind in ((self.site, "template"), (self.other, "figma")):
            with self.subTest(kind=kind):
                origin = {"kind": kind, "ref": str(uuid4()), "version": "1"}
                resolver = Mock(return_value=source)
                created = creer_brouillon(self.user, site.pk, origin, resolve_origin=resolver)
                self.assertEqual(resolver.call_count, 1)
                self.assertEqual(str(resolver.call_args.args[0]), str(site.pk))
                self.assertEqual(resolver.call_args.args[1], origin)
                self.assertEqual(source, original)
                copied = created["document"]
                self.assertTrue(occurrence_ids(copied).isdisjoint(occurrence_ids(source)))
                self.assertEqual(copied["pages"][1]["parent_id"], copied["pages"][0]["id"])
                self.assertEqual(created["origin"], origin)
                copies.append(occurrence_ids(copied))
                # The structured editor and canvas read the same stored revision independently.
                structured = lire_brouillon(self.user, site.pk)
                visual = lire_revision(self.user, site.pk, created["id"])
                self.assertEqual(structured, visual)
                self.assertEqual(structured["document"], copied)
                moved = deepcopy(copied)
                moved["pages"][0]["sections"][0]["blocks"].reverse()
                updated = enregistrer_brouillon(self.user, site.pk, created["id"], moved)
                self.assertEqual(updated["document"], moved)
                self.assertEqual(updated["origin"], origin)
                self.assertEqual(lire_revision(self.user, site.pk, created["id"])["document"], copied)
        self.assertTrue(copies[0].isdisjoint(copies[1]))

    def test_unverified_source_or_caller_supplied_external_body_is_rejected(self):
        origin = {"kind": "figma", "ref": str(uuid4()), "version": "1"}
        for options in ({}, {"resolve_origin": lambda site, source: None},
                        {"document": sample_document(), "resolve_origin": lambda site, source: sample_document()}):
            with self.subTest(options=list(options)):
                with self.assertRaises(ValidationError):
                    creer_brouillon(self.user, self.site.pk, origin, **options)
        self.assertFalse(CompositionRevision.objects.exists())

    def test_cross_site_read_write_and_revocation(self):
        first = self.blank()
        other_grant = SiteGrant.objects.create(site=self.other, user=self.user, level="manage")
        foreign = creer_brouillon(self.user, self.other.pk, {"kind": "blank"})
        other_grant.delete()
        ClientGrant.objects.create(client=self.owner, user=self.user, level="manage")
        for site_id in (self.other.pk, uuid4()):
            with self.assertRaises(Http404):
                lire_brouillon(self.user, site_id)
            with self.assertRaises(Http404):
                creer_brouillon(self.user, site_id, {"kind": "blank"})
        for revision in (foreign["id"], str(uuid4())):
            with self.assertRaises(Http404):
                lire_revision(self.user, self.site.pk, revision)
            with self.assertRaises(Conflict):
                enregistrer_brouillon(self.user, self.site.pk, revision, first["document"])
        self.grant.level = "read"
        self.grant.save(update_fields=["level"])
        self.assertEqual(lire_revision(self.user, self.site.pk, first["id"]), first)
        with self.assertRaises(PermissionDenied):
            enregistrer_brouillon(self.user, self.site.pk, first["id"], first["document"])
        self.grant.delete()
        with self.assertRaises(Http404):
            lire_revision(self.user, self.site.pk, first["id"])
        with self.assertRaises(Http404):
            enregistrer_brouillon(self.user, self.site.pk, first["id"], first["document"])
        self.assertEqual(CompositionRevision.objects.count(), 2)

    def test_inactive_out_of_group_and_anonymous_accounts(self):
        User.objects.filter(pk=self.user.pk).update(is_active=False)
        for actor in (self.user, AnonymousUser()):
            with self.assertRaises((Http404, PermissionDenied)):
                lire_brouillon(actor, self.site.pk)
            with self.assertRaises((Http404, PermissionDenied)):
                creer_brouillon(actor, self.site.pk, {"kind": "blank"})
        User.objects.filter(pk=self.user.pk).update(is_active=True)
        self.user.groups.clear()
        with self.assertRaises((Http404, PermissionDenied)):
            creer_brouillon(self.user, self.site.pk, {"kind": "blank"})

    def test_invalid_retries_and_rollback_keep_head(self):
        first = self.blank()
        with self.assertRaises(Conflict):
            self.blank()
        with self.assertRaises(ValidationError):
            enregistrer_brouillon(self.user, self.site.pk, first["id"], {"schema_version": 1})

        def interrupted_save(**kwargs):
            raise RuntimeError("Interruption simulée")

        post_save.connect(interrupted_save, sender=CompositionRevision)
        try:
            with self.assertRaisesRegex(RuntimeError, "Interruption simulée"):
                enregistrer_brouillon(self.user, self.site.pk, first["id"], first["document"])
        finally:
            post_save.disconnect(interrupted_save, sender=CompositionRevision)
        self.assertEqual(lire_brouillon(self.user, self.site.pk), first)
        second = enregistrer_brouillon(self.user, self.site.pk, first["id"], first["document"])
        with self.assertRaises(Conflict):
            enregistrer_brouillon(self.user, self.site.pk, first["id"], first["document"])
        self.assertEqual(lire_brouillon(self.user, self.site.pk), second)
        self.assertEqual(CompositionRevision.objects.count(), 2)

    def test_unknown_schema_returns_only_metadata_and_cannot_be_overwritten(self):
        first = self.blank()
        unknown = {"schema_version": 9, "extension": "Données à préserver"}
        CompositionRevision.objects.filter(pk=first["id"]).update(document=unknown)
        for result in (lire_brouillon(self.user, self.site.pk),
                       lire_revision(self.user, self.site.pk, first["id"])):
            self.assertEqual(result["id"], first["id"])
            self.assertEqual(result["number"], 1)
            self.assertEqual(result["status"], "incompatible")
            self.assertEqual(result["schema_version"], 9)
            self.assertIsNone(result.get("document"))
        with self.assertRaises(ValidationError):
            enregistrer_brouillon(self.user, self.site.pk, first["id"], first["document"])
        self.assertEqual(CompositionRevision.objects.get().document, unknown)

    def test_resource_resolution_is_scoped_and_has_uniform_errors(self):
        first = self.blank()
        owned, foreign, missing = (str(uuid4()) for _ in range(3))
        owners = {owned: self.site.pk, foreign: self.other.pk}
        sample = sample_document()
        block = sample["pages"][0]["sections"][0]["blocks"][0]
        block["definition"] = {"scope": "site", "key": "photo", "version": 1}

        def definition(site_id, scope, key, version):
            if site_id == self.site.pk and (scope, key, version) == ("site", "photo", 1):
                return {"photo": "media"}
            return None

        def resource(site_id, kind, ref_id):
            return kind == "media" and owners.get(ref_id) == site_id

        options = {"resolve_definition": definition, "resolve_reference": resource}
        failures = []
        for ref_id in (foreign, missing):
            block["props"] = {"photo": {"kind": "media", "ref_id": ref_id}}
            with self.assertRaises(ValidationError) as caught:
                enregistrer_brouillon(self.user, self.site.pk, first["id"], sample, **options)
            failures.append(str(caught.exception))
            self.assertNotIn(ref_id, str(caught.exception))
        self.assertEqual(failures[0], failures[1])
        self.assertEqual(lire_brouillon(self.user, self.site.pk), first)
        block["props"] = {"photo": {"kind": "media", "ref_id": owned}}
        saved = enregistrer_brouillon(self.user, self.site.pk, first["id"], sample, **options)
        self.assertEqual(saved["document"], sample)


@skipUnlessDBFeature("has_select_for_update")
class ConcurrentDraftTests(TransactionTestCase):
    def setUp(self):
        client = Client.objects.create(display_name="Maison Exemple", client_type="COMPANY")
        self.site = Site.objects.create(client=client, name="Ateliers")
        group = Group.objects.create(name=OPERATOR_GROUP)
        self.actors = []
        for name in ("Alice", "Boris"):
            actor = User.objects.create_user(name)
            actor.groups.add(group)
            SiteGrant.objects.create(site=self.site, user=actor, level="manage")
            self.actors.append(actor)

    def race(self, command):
        gate = Barrier(2, timeout=12)

        def worker(actor):
            try:
                gate.wait()
                return command(actor)
            except Conflict:
                return None
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            attempts = [pool.submit(worker, actor) for actor in self.actors]
            results = [attempt.result(timeout=20) for attempt in attempts]
        winners = [result for result in results if result is not None]
        self.assertEqual(len(winners), 1)
        return winners[0]

    def test_two_initial_creations_share_one_head(self):
        winner = self.race(lambda actor: creer_brouillon(actor, self.site.pk, {"kind": "blank"}))
        self.assertEqual(CompositionRevision.objects.count(), 1)
        self.assertEqual(winner["number"], 1)
        self.assertEqual(lire_brouillon(self.actors[0], self.site.pk), winner)

    def test_two_saves_on_same_base_commit_once(self):
        first = creer_brouillon(self.actors[0], self.site.pk, {"kind": "blank"})

        def save(actor):
            changed = deepcopy(first["document"])
            changed["pages"][0]["title"] = actor.username
            return enregistrer_brouillon(actor, self.site.pk, first["id"], changed)

        winner = self.race(save)
        self.assertEqual(CompositionRevision.objects.count(), 2)
        self.assertEqual(winner["parent_id"], first["id"])
        self.assertEqual(winner["number"], 2)
        self.assertEqual(lire_brouillon(self.actors[0], self.site.pk), winner)
        self.assertEqual(lire_revision(self.actors[0], self.site.pk, first["id"]), first)

    def test_different_operators_can_write_different_sites_independently(self):
        other = Site.objects.create(client=self.site.client, name="Deuxième atelier")
        SiteGrant.objects.create(site=other, user=self.actors[1], level="manage")

        def create_on_other_site():
            try:
                with transaction.atomic():
                    with connections["default"].cursor() as cursor:
                        cursor.execute("SET LOCAL lock_timeout = '2s'")
                    return creer_brouillon(self.actors[1], other.pk, {"kind": "blank"})
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=1) as pool, transaction.atomic():
            creer_brouillon(self.actors[0], self.site.pk, {"kind": "blank"})
            result = pool.submit(create_on_other_site).result(timeout=10)
            self.assertEqual(result["site_id"], str(other.pk))
