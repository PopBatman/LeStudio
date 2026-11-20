from concurrent.futures import ThreadPoolExecutor
from threading import Event
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.db import connections
from django.test import TransactionTestCase, skipUnlessDBFeature
from django.utils import timezone

from composition.editorial import verifier_article
from composition.models import EditorialObservation
from raccordement.models import SiteConnection
from registre.models import Client, Site, SiteGrant
from registre.services import Conflict
from workspace.access import OPERATOR_GROUP


@skipUnlessDBFeature("has_select_for_update")
class EditorialRaceTests(TransactionTestCase):
    def test_late_read_from_separate_connection_cannot_overwrite_new_observation(self):
        client = Client.objects.create(client_type="COMPANY", display_name="Essai")
        site = Site.objects.create(client=client, name="Essai")
        actor = User.objects.create_user("gestion")
        actor.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        SiteGrant.objects.create(site=site, user=actor, level="manage")
        profile = SimpleNamespace(engine_version="1.1", image_digest="digest", site_id=site.pk, instance_id=uuid4())
        now = timezone.now()
        SiteConnection.objects.create(site=site, instance_id=profile.instance_id, confirmed_profile="test",
            attempt_id=uuid4(), confirmed_at=now, started_at=now, expires_at=now, finished_at=now,
            diagnostic="connected", versions={"engine_version":"1.1","image_digest":"digest","capabilities":["editorial.published.v1"]})
        waiting, release = Event(), Event()

        def read(profile, page):
            if waiting.is_set():
                return "102"
            waiting.set()
            self.assertTrue(release.wait(10))
            return "101"

        def slow_call():
            try:
                verifier_article(actor, site.pk, 42)
            finally:
                connections.close_all()

        with (patch("composition.editorial.load_profile", return_value=profile),
              patch("composition.editorial.read_published_article", side_effect=read),
              ThreadPoolExecutor(max_workers=1) as pool):
            first = pool.submit(slow_call)
            try:
                self.assertTrue(waiting.wait(10))
                second = verifier_article(actor, site.pk, 42)
            finally:
                release.set()
            with self.assertRaises(Conflict):
                first.result(timeout=10)
        obs = EditorialObservation.objects.get(site=site)
        self.assertEqual((str(obs.attempt), obs.published_revision), (second["token"], "102"))
