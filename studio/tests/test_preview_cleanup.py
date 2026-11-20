from datetime import timedelta
from io import StringIO
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from composition.models import CompositionRevision, PreviewTicket
from registre.models import Client, Site


class PreviewCleanupTests(TestCase):
    def test_only_deletes_expired_receipts_including_exact_deadline(self):
        now = timezone.now()
        user = User.objects.create_user("lecture")
        owner = Client.objects.create(display_name="Site test", client_type="COMPANY")
        site = Site.objects.create(client=owner, name="Atelier")
        revision = CompositionRevision.objects.create(site=site, number=1, origin={"kind": "blank"}, document={})
        session = Session.objects.create(session_key="session-test", session_data="", expire_date=now + timedelta(hours=1))
        receipts = [PreviewTicket.objects.create(operator=user, revision=revision, session=session, page_id=uuid4(),
                        fingerprint="a" * 64, created_at=now - timedelta(minutes=10),
                        expires_at=now + timedelta(seconds=seconds)) for seconds in (-1, 0, 1)]
        with patch("composition.management.commands.purge_apercus.timezone.now", return_value=now):
            for count in (2, 0):
                output = StringIO()
                call_command("purge_apercus", stdout=output)
                self.assertIn(str(count), output.getvalue())
                self.assertEqual(list(PreviewTicket.objects.values_list("pk", flat=True)), [receipts[-1].pk])
        self.assertTrue(CompositionRevision.objects.filter(pk=revision.pk).exists())
        self.assertTrue(Session.objects.filter(pk=session.pk).exists())
