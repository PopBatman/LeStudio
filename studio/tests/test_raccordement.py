from concurrent.futures import ThreadPoolExecutor
from threading import Event
from uuid import uuid4
from unittest.mock import patch
from types import SimpleNamespace

from django.contrib.auth.models import User, Group
from django.test import TestCase, TransactionTestCase, skipUnlessDBFeature
from django.db import connections
from registre.models import Client, Site, SiteGrant
from workspace.access import OPERATOR_GROUP
from raccordement.models import SiteConnection
from raccordement.services import LinkError, inspect_link, verify_link


class LinkTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("operateur")
        self.user.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        client = Client.objects.create(display_name="Atelier", client_type="COMPANY")
        self.site = Site.objects.create(client=client, name="Vitrine")
        self.grant = SiteGrant.objects.create(site=self.site, user=self.user, level="manage")
        self.profile = SimpleNamespace(site_id=self.site.pk, instance_id=uuid4(), alias="atelier")
        self.versions = dict(engine_version="1.0.0", wagtail_version="7.4", image_digest="sha256:"+"a"*64,
                             contract_major=1, contract_minor=0)

    def verify(self):
        return verify_link(self.user, self.site.pk, "atelier")

    def test_unconnected_and_read_only(self):
        self.assertEqual(inspect_link(self.user,self.site.pk)["status"],"unlinked")
        self.grant.level = "read"
        self.grant.save()
        with patch("raccordement.services.load_profile") as profile:
            with self.assertRaisesRegex(LinkError, "forbidden"):
                self.verify()
            profile.assert_not_called()
        self.assertFalse(SiteConnection.objects.exists())

    def test_success_reverification_and_identity_failure_preserves_association(self):
        with patch("raccordement.services.load_profile", return_value=self.profile), patch(
            "raccordement.services.probe", return_value=self.versions
        ):
            original = self.verify()
            refreshed = self.verify()
        self.assertEqual(original["status"], "connected")
        self.assertEqual(refreshed["confirmed"]["instance_id"], str(self.profile.instance_id))
        self.assertNotEqual(original["attempt"]["id"], refreshed["attempt"]["id"])
        self.profile.site_id = uuid4()
        with patch("raccordement.services.load_profile", return_value=self.profile), patch(
            "raccordement.services.probe"
        ) as network:
            with self.assertRaisesRegex(LinkError, "identity_mismatch"):
                self.verify()
            network.assert_not_called()
        state = inspect_link(self.user, self.site.pk)
        self.assertEqual(state["confirmed"], refreshed["confirmed"])
        self.assertEqual(state["status"], "identity_mismatch")

    def test_only_current_attempt_confirms_and_revalidates_actor(self):
        def revoke(profile):
            with self.assertRaisesRegex(LinkError, "in_progress"):
                self.verify()
            self.grant.delete()
            return self.versions

        with patch("raccordement.services.load_profile", return_value=self.profile), patch(
            "raccordement.services.probe", side_effect=revoke
        ):
            with self.assertRaisesRegex(LinkError, "not_found"):
                self.verify()
        row = SiteConnection.objects.get()
        self.assertIsNone(row.instance_id)
        self.assertEqual(row.diagnostic, "not_found")

    def test_expired_attempt_replaced_cannot_overwrite_new_result(self):
        from datetime import timedelta
        from django.utils import timezone

        def recover(profile):
            SiteConnection.objects.update(expires_at=timezone.now()-timedelta(seconds=1))
            with patch("raccordement.services.probe", return_value=self.versions):
                self.verify()
            return dict(self.versions, engine_version="obsolete")

        with patch("raccordement.services.load_profile", return_value=self.profile), patch(
            "raccordement.services.probe", side_effect=recover
        ):
            with self.assertRaisesRegex(LinkError, "superseded"):
                self.verify()
        row = SiteConnection.objects.get()
        self.assertEqual(row.versions, self.versions)
        self.assertEqual(row.diagnostic, "connected")

    def test_competing_site_cannot_claim_existing_instance(self):
        with patch("raccordement.services.load_profile", return_value=self.profile), patch(
            "raccordement.services.probe", return_value=self.versions
        ):
            self.verify()
            other = Site.objects.create(client=self.site.client, name="Autre")
            SiteGrant.objects.create(site=other, user=self.user, level="manage")
            self.profile.site_id = other.pk
            with self.assertRaisesRegex(LinkError, "association_conflict"):
                verify_link(self.user, other.pk, "atelier")
        self.assertIsNone(SiteConnection.objects.get(site=other).instance_id)



@skipUnlessDBFeature("has_select_for_update")
class ConcurrentLinkTests(TransactionTestCase):
    def test_parallel_request_observes_reservation(self):
        actor = User.objects.create_user("gestion")
        actor.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        client = Client.objects.create(display_name="Commun", client_type="COMPANY")
        site = Site.objects.create(client=client, name="Premier")
        SiteGrant.objects.create(site=site, user=actor, level="manage")
        profile = SimpleNamespace(site_id=site.pk, instance_id=uuid4(), alias="premier")
        started, resume = Event(), Event()

        def read_remote(profile):
            started.set()
            self.assertTrue(resume.wait(timeout=10))
            return {"contract_major": 1}

        def first_request():
            try:
                return verify_link(actor, site.pk, "premier")
            finally:
                connections.close_all()

        with patch("raccordement.services.load_profile", return_value=profile), patch(
            "raccordement.services.probe", side_effect=read_remote
        ) as probe, ThreadPoolExecutor(max_workers=1) as pool:
            first = pool.submit(first_request)
            try:
                self.assertTrue(started.wait(timeout=10))
                self.assertEqual(inspect_link(actor, site.pk)["status"], "checking")
                with self.assertRaisesRegex(LinkError, "in_progress"):
                    verify_link(actor, site.pk, "premier")
            finally:
                resume.set()
            self.assertEqual(first.result(timeout=10)["status"], "connected")
            probe.assert_called_once()
