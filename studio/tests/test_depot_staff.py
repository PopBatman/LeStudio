from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import TestCase, override_settings
from django.urls import reverse

from registre.models import Client, Site, SiteGrant
from workspace.access import OPERATOR_GROUP


@override_settings(STUDIO_PORTAL_ORIGIN="https://depots.example.test")
class StaffDepositTests(TestCase):
    def setUp(self):
        self.actor = User.objects.create_user("responsable")
        self.actor.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        client = Client.objects.create(display_name="Client fictif", client_type="COMPANY")
        self.site = Site.objects.create(name="Atelier fictif", client=client)
        self.other = Site.objects.create(name="Autre atelier", client=client)
        self.grant = SiteGrant.objects.create(user=self.actor, site=self.site, level="manage")
        self.client.force_login(self.actor)
        self.index = f"/sites/{self.site.pk}/depots/"
        self.issue = self.index + "invitations/creer/"

    def make_submission(self, invitation, version=1):
        from depots.models import Submission

        return Submission.objects.create(invitation=invitation, version=version,
            request_id=uuid4(), figma_url="https://www.figma.com/design/TestFile",
            comment="Remise fictive")

    def test_site_entry_and_single_disclosure(self):
        self.assertContains(self.client.get(reverse("registre:site", args=[self.site.pk])), "Dernier dépôt Figma")
        self.assertContains(self.client.get(self.index), "Créer une invitation de 7 jours")
        response = self.client.post(self.issue)
        self.assertEqual(response.status_code, 200)
        secret = response.context["code"]
        self.assertContains(response, f"https://depots.example.test/depot/#{secret}")
        self.assertIn("no-store", response.headers["Cache-Control"])
        self.assertEqual(response.headers["Referrer-Policy"], "same-origin")
        self.assertNotContains(self.client.get(self.index), secret)
        self.assertEqual(self.client.get(self.issue).status_code, 405)
        self.assertNotContains(self.client.get(self.index), self.other.name)

    def test_revocation_requires_confirmation_and_current_management(self):
        invitation = self.client.post(self.issue).context["invitation"]
        url = reverse("registre:depot-revoke", args=[self.site.pk, invitation.pk])
        self.assertContains(self.client.get(url), "Confirmer la révocation")
        invitation.refresh_from_db()
        self.assertIsNone(invitation.revoked_at)
        self.grant.level = "read"
        self.grant.save()
        self.assertNotContains(self.client.get(self.index), "Créer une invitation de 7 jours")
        self.assertEqual(self.client.post(self.issue).status_code, 403)
        self.assertEqual(self.client.post(url).status_code, 403)
        self.grant.level = "manage"
        self.grant.save()
        self.assertEqual(self.client.post(url).status_code, 302)
        invitation.refresh_from_db()
        self.assertIsNotNone(invitation.revoked_at)
        self.assertContains(self.client.get(self.index), "Révoquée")

    def test_detail_and_latest_are_scoped_and_cursor_is_checked(self):
        from depots.models import Submission

        invitation = self.client.post(self.issue).context["invitation"]
        row = self.make_submission(invitation)
        site_url = reverse("registre:site", args=[self.site.pk])
        self.assertContains(self.client.get(site_url), "Version 1")
        url = reverse("registre:depot-submission", args=[self.site.pk, row.pk])
        detail = self.client.get(url)
        self.assertContains(detail, row.figma_url)
        self.assertContains(detail, "Remise fictive")
        self.assertEqual(self.client.get(self.index, {"cursor": "absent"}).status_code, 400)
        self.assertEqual(self.client.get(reverse("registre:depot-submission", args=[self.other.pk, row.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse("registre:depot-submission", args=[self.site.pk, uuid4()])).status_code, 404)
        self.grant.delete()
        self.assertEqual(self.client.get(self.index).status_code, 404)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertTrue(Submission.objects.filter(pk=row.pk).exists())

    def test_erase_needs_management_and_clears_the_site_signal(self):
        invitation = self.client.post(self.issue).context["invitation"]
        row = self.make_submission(invitation)
        url = reverse("registre:depot-erase", args=[self.site.pk, row.pk])
        self.assertContains(self.client.get(url), "Confirmer l’effacement")
        self.grant.level = "read"
        self.grant.save()
        self.assertEqual(self.client.post(url).status_code, 403)
        self.grant.level = "manage"
        self.grant.save()
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertContains(self.client.get(reverse("registre:site", args=[self.site.pk])),
                            "Aucune version reçue pour ce site")
        detail = reverse("registre:depot-submission", args=[self.site.pk, row.pk])
        self.assertEqual(self.client.get(detail).status_code, 404)

    def test_next_cursor_preserves_scope_and_order(self):
        first = self.client.post(self.issue).context["invitation"]
        second = self.client.post(self.issue).context["invitation"]
        oldest = self.make_submission(first)
        for version in range(1, 21):
            self.make_submission(second, version)
        page = self.client.get(self.index)
        self.assertContains(page, "Versions suivantes")
        self.assertEqual(len(page.context["submissions"]), 20)
        last_page = self.client.get(self.index, {"cursor": page.context["next_cursor"]})
        self.assertEqual([r.pk for r in last_page.context["submissions"]], [oldest.pk])
        self.assertNotContains(last_page, "Versions suivantes")
