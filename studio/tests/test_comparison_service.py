from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from datetime import timedelta
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from django.contrib.sessions.backends.db import SessionStore
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import connections
from django.http import Http404
from django.test import TestCase, TransactionTestCase, skipUnlessDBFeature
from django.utils import timezone
from PIL import Image, PngImagePlugin

from composition import preview_views
from composition.models import CompositionRevision
from depots import comparison, imports, services
from depots.models import ComparisonDecision, FrameReference, Submission
from registre.services import Conflict
from .test_figma_imports import ImportFixtures


def png(size=(120, 80), color="green"):
    image = Image.new("RGB", size, color)
    out = BytesIO()
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("comment", "private-source-metadata")
    image.save(out, format="PNG", pnginfo=metadata)
    out.seek(0)
    return out


class ComparisonFixtures(ImportFixtures):
    def setUp(self):
        super().setUp()
        row = self.review()
        self.analysis = imports.confirm(*self.args, row.token)
        self.page = self.analysis.mapping["2:3"]
        self.analysis.observation["frames"][0].update(width=60, height=40)
        self.analysis.save(update_fields=["observation"])
        session = SessionStore()
        session.create()
        self.request = SimpleNamespace(user=self.manager, session=session)
        self.render = {"html":"page", "manifest":{"instance_id": str(uuid4()),
                                                 "block_ids":[self.analysis.mapping["2:4"]]}}
        self.ticket = preview_views.issue(self.request, self.analysis.result_revision_id, self.page,
                                          timezone.now(), self.render)
        self.preview = patch("composition.preview_views.render_preview", return_value=self.render).start()

    def attach(self, upload=None, **kwargs):
        kwargs.setdefault("revision_id", self.analysis.result_revision_id)
        return comparison.attach_reference(self.manager, self.site.pk, self.analysis.pk, self.page, "2:3",
                                           "v1", "mobile", upload or png(), **kwargs)

    def decide(self, ref, **kwargs):
        data = dict(reference_id=ref.pk, ticket_id=self.ticket.pk, revision_id=self.analysis.result_revision_id,
                    format="mobile", width=60, target="", kind="accepted", note="Alignement confirmé.",
                    previous="", key=uuid4())
        data.update(kwargs)
        return comparison.save_decision(self.request, self.site.pk, self.analysis.pk, self.page, "2:3", **data)


class ComparisonServiceTests(ComparisonFixtures, TestCase):
    def test_png_normalized_private_and_replaced(self):
        with self.assertRaises(Conflict):
            self.attach(revision_id=uuid4())
        reference = self.attach()
        payload = comparison.reference_png(self.manager, self.site.pk, reference.pk)
        self.assertNotIn(b"private-source-metadata", payload)
        self.assertEqual(Image.open(BytesIO(payload)).size, (120, 80))
        with self.assertRaises(Http404):
            comparison.reference_png(self.manager, self.other.pk, reference.pk)
        with self.assertRaises(Conflict):
            self.attach()
        latest = self.attach(previous=reference.pk)
        self.assertNotEqual(reference.pk, latest.pk)
        with self.assertRaises(Http404):
            comparison.reference_png(self.manager, self.site.pk, reference.pk)
        self.grant.level = "read"
        self.grant.save()
        with self.assertRaises(PermissionDenied):
            comparison.reference_png(self.manager, self.site.pk, latest.pk)

    def test_malformed_oversized_or_wrong_aspect_refused(self):
        for upload in (BytesIO(b"other file"), BytesIO(png().getvalue()[:-18]), png((200, 10))):
            with self.assertRaises(ValidationError):
                self.attach(upload)
        self.assertFalse(FrameReference.objects.exists())

    def test_decision_replay_replacement_and_concurrent_base(self):
        ref = self.attach()
        key = uuid4()
        decision = self.decide(ref, key=key)
        self.assertEqual(self.decide(ref, key=key).pk, decision.pk)
        with self.assertRaises(Conflict):
            self.decide(ref, key=key, note="Autre")
        with self.assertRaises(Conflict):
            self.decide(ref)
        self.decide(ref, previous=decision.pk, kind="correct", note="Reprendre.")
        self.assertEqual(ComparisonDecision.objects.count(), 2)
        self.assertEqual(CompositionRevision.objects.count(), 1)
        self.attach(previous=ref.pk)
        with self.assertRaises(Conflict):
            self.decide(ref, key=key)

    def test_wrong_width_target_expiry_and_source_erasure(self):
        ref = self.attach()
        with self.assertRaises(ValidationError):
            self.decide(ref, width=120)
        with self.assertRaises(ValidationError):
            self.decide(ref, target=uuid4())
        self.decide(ref)
        self.ticket.expires_at = timezone.now()
        self.ticket.save()
        with self.assertRaises(Conflict):
            self.decide(ref)
        services.erase_submission(*self.args)
        self.assertFalse(FrameReference.objects.exists())
        self.assertFalse(ComparisonDecision.objects.exists())
        self.assertEqual(CompositionRevision.objects.count(), 1)

    def test_source_ttl_even_before_periodic_purge(self):
        ref = self.attach()
        self.decide(ref)
        Submission.objects.update(created_at=timezone.now() - timedelta(days=91))
        with self.assertRaises(Http404):
            comparison.reference_png(self.manager, self.site.pk, ref.pk)
        services.purge()
        self.assertFalse(FrameReference.objects.exists())
        self.assertFalse(ComparisonDecision.objects.exists())


class ConcurrentDecisionTests(ComparisonFixtures, TransactionTestCase):
    def setUp(self):
        # TransactionTestCase flushes the catalogue installed by data migrations.
        from composition.catalogue import installer_version
        from composition.catalogue_v1 import TITLES

        for key, title in TITLES.items():
            installer_version(None, key, 1, title, key)
        super().setUp()

    @skipUnlessDBFeature("has_select_for_update")
    def test_two_operators_deciding_on_same_unreviewed_occurrence(self):
        from django.contrib.auth.models import User
        from registre.models import SiteGrant

        ref = self.attach()
        other = User.objects.create_user("deuxieme-gestionnaire")
        other.groups.set(self.manager.groups.all())
        SiteGrant.objects.create(site=self.site, user=other, level="manage")
        session = SessionStore()
        session.create()
        request = SimpleNamespace(user=other, session=session)
        ticket = preview_views.issue(request, self.analysis.result_revision_id, self.page, timezone.now(), self.render)
        barrier = Barrier(2)

        def post(pair):
            req, receipt = pair
            try:
                barrier.wait(timeout=10)
                comparison.save_decision(req, self.site.pk, self.analysis.pk, self.page, "2:3", reference_id=ref.pk,
                                         revision_id=self.analysis.result_revision_id, ticket_id=receipt.pk,
                                         format="mobile", width=60, target="", kind="matched", note="",
                                         previous="", key=uuid4())
                return "created"
            except Conflict:
                return "conflict"
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(post, [(self.request, self.ticket), (request, ticket)]))
        self.assertCountEqual(results, ["created", "conflict"])
        self.assertEqual(ComparisonDecision.objects.count(), 1)
