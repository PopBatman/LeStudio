from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.db import connections
from django.test import TestCase, TransactionTestCase, skipUnlessDBFeature
from django.utils import timezone

from depots import imports, services
from depots.models import ImportAnalysis, Submission
from registre.services import Conflict
from composition.models import CompositionRevision
from .test_depots_domain import Fixtures


class ImportFixtures(Fixtures):
    def setUp(self):
        super().setUp()
        self.sub = services.submit(self.cap, uuid4(), self.url)
        self.args = self.manager, self.site.pk, self.sub.pk
        self.profile = SimpleNamespace(generation="profile-A")
        self.load = patch("depots.figma.load_profile", return_value=self.profile).start()
        self.inventory = patch(
            "depots.figma.inventory",
            return_value={
                "version": "v1",
                "observed_at": "2026-11-20T10:00:00Z",
                "frames": [{"id": "2:3", "name": "Écran", "page": "Page"}],
            },
        ).start()
        self.addCleanup(patch.stopall)

    def review(self, append=False):
        inv = imports.start(*self.args)
        frame = {
            "id": "2:3",
            "name": "Page source",
            "nodes": [
                {"id": "2:4", "type": "TEXT", "name": "Titre", "parent_id": "2:3", "text": "Studio fictif"},
                {"id": "2:5", "type": "VECTOR", "parent_id": "2:3", "name": "À concevoir"},
            ],
        }
        observed = {"version": "v1", "frames": [frame], "observed_at": "2026-11-20T10:00:00Z"}
        with patch("depots.figma.inspect_frames", return_value=observed):
            row = imports.select_frames(*self.args, inv.token, ["2:3"])
        decisions = {
            r["id"]: {"action": "exclude" if r["id"] == "2:5" else "accept"} for r in row.proposals
        }
        targets = [
            dict(
                group="Accueil",
                format="mobile",
                base=True,
                home=not append,
                frame_id="2:3",
                title="Invitations",
                slug="invitations" if append else "",
            )
        ]
        return imports.save_review(*self.args, row.token, decisions, targets)


class ImportTests(ImportFixtures, TestCase):
    def test_revoked_invitation_remains_eligible_but_erase_during_read_refuses(self):
        services.revoke_invitation(self.manager, self.site.pk, self.inv.pk)
        row = imports.start(*self.args)
        self.assertEqual(row.state, "inventory")

        def erase(profile):
            services.erase_submission(*self.args)
            return {"version": "v1", "frames": []}

        self.inventory.side_effect = erase
        with self.assertRaises(Http404):
            imports.current(*self.args)
        self.assertFalse(ImportAnalysis.objects.filter(submission=self.sub).exists())

    def test_withdrawn_grant_and_different_site_do_not_contact_provider(self):
        self.grant.level = "read"
        self.grant.save()
        with self.assertRaises(PermissionDenied):
            imports.start(*self.args)
        with self.assertRaises(Http404):
            imports.start(self.manager, self.other.pk, self.sub.pk)
        self.inventory.assert_not_called()

    def test_version_changes_invalidate_review_and_retention_purges_observation(self):
        row = imports.start(*self.args)
        self.inventory.return_value = {"version": "v2", "frames": []}
        with self.assertRaises(ValidationError):
            imports.current(*self.args)
        row.refresh_from_db()
        self.assertEqual(row.inventory, {})
        self.assertEqual(row.state, "failed")
        Submission.objects.filter(pk=self.sub.pk).update(created_at=timezone.now() - timedelta(days=100))
        services.purge()
        self.assertFalse(ImportAnalysis.objects.filter(pk=row.pk).exists())

    def test_apply_and_repeat_then_erase_source_keep_local_revision(self):
        row = self.review()
        result = imports.confirm(*self.args, row.token)
        again = imports.confirm(*self.args, row.token)
        self.assertEqual(again.result_revision_id, result.result_revision_id)
        self.assertEqual(again.observation, {})
        with patch("depots.figma.load_profile", side_effect=imports.figma.FigmaError("profile")):
            with self.assertRaises(ValidationError):
                imports.start(*self.args)
            self.assertEqual(imports.confirm(*self.args, row.token).result_revision_id, result.result_revision_id)
        revision = CompositionRevision.objects.get()
        page = revision.document["pages"][0]
        self.assertEqual(result.mapping["2:3"], page["id"])
        self.assertEqual(result.mapping["2:4"], page["sections"][0]["blocks"][0]["children"][0]["id"])
        self.assertEqual(revision.origin["kind"], "figma")
        services.erase_submission(*self.args)
        result.refresh_from_db()
        self.assertEqual(
            (result.observation, result.proposals, result.decisions, result.mapping), ({}, [], {}, {})
        )
        self.assertIsNone(result.submission_id)
        self.assertEqual(result.result_revision_id, revision.pk)

    def test_appending_and_stale_head(self):
        from composition.editor import creer_atelier
        from composition.services import modifier_navigation

        original = creer_atelier(self.manager, self.site.pk, "template")
        row = self.review(append=True)
        new = modifier_navigation(
            self.manager, self.site.pk, original["id"], {"action": "menu_add", "label": "Pied"}
        )
        with self.assertRaises(Conflict):
            imports.confirm(*self.args, row.token)
        self.assertEqual(CompositionRevision.objects.count(), 2)
        row = self.review(append=True)
        result = imports.confirm(*self.args, row.token)
        rev = result.result_revision
        self.assertEqual(str(rev.parent_id), new["id"])
        self.assertEqual(rev.document["pages"][:-1], original["document"]["pages"])
        self.assertEqual(rev.document["menus"], new["document"]["menus"])
        self.assertEqual(rev.document["theme"], new["document"]["theme"])
        self.assertEqual(result.mapping["2:3"], rev.document["pages"][-1]["id"])

    def test_late_remote_reads_and_removed_profiles_do_not_disclose_proposals(self):
        from depots.figma import FigmaError

        row = self.review()
        self.load.side_effect = FigmaError("profile")
        with self.assertRaises(ValidationError):
            imports.current(*self.args)
        row.refresh_from_db()
        self.assertEqual((row.observation, row.proposals, row.decisions), ({}, [], {}))


@skipUnlessDBFeature("has_select_for_update")
class ImportRaces(ImportFixtures, TransactionTestCase):
    def setUp(self):
        super().setUp()
        from composition.catalogue import installer_version
        from composition.catalogue_v1 import TITLES

        for key, title in TITLES.items():
            installer_version(None, key, 1, title, key)

    def test_two_confirmations_commit_once_after_parallel_remote_reads(self):
        row = self.review()
        gate = Barrier(2)

        def fetch(profile):
            gate.wait(timeout=8)
            return {"version": "v1", "frames": []}

        self.inventory.side_effect = fetch

        def apply():
            try:
                return imports.confirm(*self.args, row.token).result_revision_id
            finally:
                connections.close_all()

        with ThreadPoolExecutor(2) as pool:
            a = pool.submit(apply)
            b = pool.submit(apply)
            self.assertEqual(a.result(timeout=12), b.result(timeout=12))
        self.assertEqual(CompositionRevision.objects.count(), 1)

    def test_erase_or_downgrade_during_confirmation(self):
        row = self.review()

        def during_read(profile):
            self.grant.level = "read"
            self.grant.save()
            return {"version": "v1", "frames": []}

        self.inventory.side_effect = during_read
        with self.assertRaises(PermissionDenied):
            imports.confirm(*self.args, row.token)
        self.grant.level = "manage"
        self.grant.save()

        def erase(profile):
            services.erase_submission(*self.args)
            return {"version": "v1", "frames": []}

        self.inventory.side_effect = erase
        with self.assertRaises(Http404):
            imports.confirm(*self.args, row.token)
        self.assertEqual(CompositionRevision.objects.count(), 0)
        self.assertFalse(ImportAnalysis.objects.exists())
