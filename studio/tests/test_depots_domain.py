from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import connections
from django.http import Http404
from django.test import TestCase, TransactionTestCase, skipUnlessDBFeature
from django.utils import timezone

from depots import services as api
from depots.models import Invitation, Submission
from registre.models import Client, Site, SiteGrant
from registre.services import Conflict
from workspace.access import OPERATOR_GROUP


class Fixtures:
    def setUp(self):
        self.manager = User.objects.create_user("gestion")
        self.manager.groups.add(Group.objects.get_or_create(name=OPERATOR_GROUP)[0])
        client = Client.objects.create(display_name="Atelier", client_type="COMPANY")
        self.site = Site.objects.create(client=client, name="A")
        self.other = Site.objects.create(client=client, name="B")
        self.grant = SiteGrant.objects.create(site=self.site, user=self.manager, level="manage")
        self.inv, self.secret = api.create_invitation(self.manager, self.site.pk)
        self.cap, _ = api.exchange(self.secret, "127.0.0.1")
        self.url = "https://www.figma.com/design/AnExample/Atelier?node-id=2-3&t=tracking"


class DepotDomainTests(Fixtures, TestCase):
    def test_scope_receipt_and_idempotency(self):
        key = uuid4()
        first = api.submit(self.cap, key, self.url, "Vue mobile")
        self.assertEqual(first.figma_url, "https://www.figma.com/design/AnExample?node-id=2-3")
        self.assertEqual(api.submit(self.cap, key, self.url, "Vue mobile").pk, first.pk)
        with self.assertRaises(Conflict):
            api.submit(self.cap, key, self.url, "Autre message")
        second = api.submit(self.cap, uuid4(), self.url)
        self.assertEqual(second.version, 2)
        self.assertEqual(api.receipt(self.cap, second.pk).pk, second.pk)
        self.assertEqual(api.latest_submission(self.manager, self.site.pk).pk, second.pk)
        self.assertEqual(api.source_for_import(self.manager, self.site.pk, first.pk)["version"], 1)
        with self.assertRaises(Http404):
            api.submission_for(self.manager, self.other.pk, first.pk)
        self.grant.level = "read"
        self.grant.save()
        with self.assertRaises(PermissionDenied):
            api.source_for_import(self.manager, self.site.pk, first.pk)
        with self.assertRaises(PermissionDenied):
            api.revoke_invitation(self.manager, self.site.pk, self.inv.pk)
        self.grant.delete()
        with self.assertRaises(Http404):
            api.latest_submission(self.manager, self.site.pk)

    def test_revoked_expired_and_archived(self):
        Client.objects.update(archived_at=timezone.now())
        first = api.submit(self.cap, uuid4(), self.url)
        api.revoke_invitation(self.manager, self.site.pk, self.inv.pk)
        api.revoke_invitation(self.manager, self.site.pk, self.inv.pk)
        with self.assertRaises(api.InvalidInvitation):
            api.submit(self.cap, uuid4(), self.url)
        with self.assertRaises(api.InvalidInvitation):
            api.receipt(self.cap, first.pk)
        inv, secret = api.create_invitation(self.manager, self.site.pk)
        cap, _ = api.exchange(secret, "127.0.0.1")
        with self.assertRaises(Http404):
            api.receipt(cap, first.pk)
        self.assertEqual(api.submit(cap, uuid4(), self.url).version, 1)
        Invitation.objects.filter(pk=inv.pk).update(expires_at=timezone.now())
        with self.assertRaises(api.InvalidInvitation):
            api.submit(cap, uuid4(), self.url)
        self.assertEqual(api.submission_for(self.manager, self.site.pk, first.pk).pk, first.pk)

    def test_five_per_window_and_exchange_quota(self):
        for i in range(5):
            key = uuid4()
            row = api.submit(self.cap, key, self.url)
        with self.assertRaises(api.RateLimited) as caught:
            api.submit(self.cap, uuid4(), self.url)
        self.assertGreater(caught.exception.retry_after, 0)
        self.assertEqual(api.submit(self.cap, key, self.url).pk, row.pk)
        for i in range(10):
            with self.assertRaises(api.InvalidInvitation):
                api.exchange("invalid", "192.0.2.1")
        with self.assertRaises(api.RateLimited):
            api.exchange(self.secret, "192.0.2.1")

    def test_cursor_and_lifetime_cap(self):
        submissions = []
        for i in range(20):
            row = api.submit(self.cap, uuid4(), self.url)
            submissions.append(row)
            # Advance submissions out of the short rate window without waiting.
            Submission.objects.filter(pk=row.pk).update(created_at=timezone.now()-timedelta(minutes=11))
        with self.assertRaises(api.RateLimited) as caught:
            api.submit(self.cap, uuid4(), self.url)
        self.assertIsNone(caught.exception.retry_after)
        inv, secret = api.create_invitation(self.manager, self.site.pk)
        cap, _ = api.exchange(secret, "127.0.0.1")
        newest = api.submit(cap, uuid4(), self.url)
        first_page, cursor = api.submissions(self.manager, self.site.pk)
        self.assertEqual(len(first_page), 20)
        self.assertEqual(first_page[0].pk, newest.pk)
        second_page, end = api.submissions(self.manager, self.site.pk, cursor)
        self.assertIsNone(end)
        self.assertEqual(len(second_page), 1)
        self.assertEqual({r.pk for r in first_page+second_page}, {r.pk for r in submissions+[newest]})
        SiteGrant.objects.create(user=self.manager, site=self.other, level="manage")
        with self.assertRaises(ValidationError):
            api.submissions(self.manager, self.other.pk, cursor)

    def test_erase_command_and_restore_purge(self):
        from io import StringIO
        from django.core.management import call_command
        from django.core.management.base import CommandError

        first = api.submit(self.cap, uuid4(), self.url, "Remise à effacer")
        survivor = api.submit(self.cap, uuid4(), self.url, "Autre remise")
        # Simulate re-applying the recorded targeted erasure after restoring a backup.
        for _ in range(2):
            call_command("purge_depots", operateur=self.manager.username, site=str(self.site.pk),
                         soumission=str(first.pk), stdout=StringIO())
        with self.assertRaises(Http404):
            api.submission_for(self.manager, self.site.pk, first.pk)
        self.assertEqual(api.latest_submission(self.manager, self.site.pk).pk, survivor.pk)
        with self.assertRaises(CommandError):
            call_command("purge_depots", site=str(self.site.pk), stdout=StringIO())

    def test_purge_and_rejected_input(self):
        for url in ["http://www.figma.com/file/A", "https://figma.com.example.org/file/A",
                    "https://www.figma.com/file/A?node-id=bogus"]:
            with self.assertRaises(ValidationError):
                api.submit(self.cap, uuid4(), url)
        with self.assertRaises(ValidationError):
            api.submit(self.cap, uuid4(), self.url, "x"*2001)
        key = uuid4()
        old = api.submit(self.cap, key, self.url)
        api.erase_submission(self.manager, self.site.pk, old.pk)
        with self.assertRaises(Conflict):
            api.submit(self.cap, key, self.url)
        with self.assertRaises(Http404):
            api.source_for_import(self.manager, self.site.pk, old.pk)
        second = api.submit(self.cap, uuid4(), self.url)
        self.assertEqual(second.version, 2)
        Submission.objects.filter(pk=second.pk).update(created_at=timezone.now()-timedelta(days=91))
        self.assertIsNone(api.latest_submission(self.manager, self.site.pk))
        api.purge()
        api.purge()
        self.assertFalse(Submission.objects.filter(pk=second.pk).exclude(figma_url="").exists())


@skipUnlessDBFeature("has_select_for_update")
class DepotRaces(Fixtures, TransactionTestCase):
    def parallel(self, *work):
        barrier = Barrier(len(work))
        def perform(function):
            try:
                barrier.wait(timeout=5)
                return function()
            finally:
                connections.close_all()
        with ThreadPoolExecutor(max_workers=len(work)) as pool:
            futures = [pool.submit(perform, function) for function in work]
            return [future.result(timeout=10) for future in futures]

    def test_repeat_and_independent_concurrent_versions(self):
        key = uuid4()
        call = lambda: api.submit(self.cap, key, self.url).pk
        a,b = self.parallel(call,call)
        self.assertEqual(a,b)
        new = lambda: api.submit(self.cap, uuid4(), self.url).version
        self.assertEqual(sorted(self.parallel(new,new)),[2,3])

    def test_revocation_serializes_with_deposit(self):
        def send():
            try:
                return api.submit(self.cap, uuid4(), self.url).pk
            except api.InvalidInvitation:
                return None
        def revoke():
            api.revoke_invitation(self.manager, self.site.pk, self.inv.pk)
        result,_ = self.parallel(send,revoke)
        self.assertEqual(Submission.objects.count(),int(result is not None))
        with self.assertRaises(api.InvalidInvitation):
            api.submit(self.cap, uuid4(), self.url)
