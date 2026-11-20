from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import Client as Browser, TestCase, override_settings
from django.utils import timezone

from depots import services
from depots.models import Submission
from registre.models import Client, Site, SiteGrant
from workspace.access import OPERATOR_GROUP


@override_settings(STUDIO_PORTAL_ORIGIN="https://portail.example", STUDIO_PORTAL_CONTACT="studio@example.invalid")
class GuestPortalTests(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user("gestion")
        self.manager.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        owner = Client.objects.create(display_name="Client privé", client_type="COMPANY")
        self.site = Site.objects.create(client=owner, name="Portfolio")
        SiteGrant.objects.create(site=self.site, user=self.manager, level="manage")
        self.invitation, self.secret = services.create_invitation(self.manager, self.site.pk)
        self.browser = Browser(enforce_csrf_checks=True)

    def exchange(self, secret):
        self.browser.get("/depot/")
        return self.browser.post("/depot/", {
            "code": secret, "csrfmiddlewaretoken": self.browser.cookies["csrftoken"].value,
        })

    def payload(self):
        response = self.browser.get("/depot/version/")
        self.assertContains(response, "Déposer une maquette")
        return {
            "request_id": response.context["request_id"],
            "csrfmiddlewaretoken": self.browser.cookies["csrftoken"].value,
            "figma_url": "https://www.figma.com/design/ABCDE/Portfolio",
            "comment": "",
        }

    def test_exchange_submission_replay_receipt_and_revocation(self):
        self.assertEqual(self.browser.post("/depot/", {"code": self.secret}).status_code, 403)
        response = self.exchange(self.secret)
        self.assertEqual(response.status_code, 303)
        cookie = response.cookies["depot_acces"]
        self.assertEqual(cookie["path"], "/depot/")
        self.assertTrue(cookie["httponly"])
        self.assertTrue(cookie["secure"])
        self.assertEqual(cookie["samesite"], "Strict")
        self.assertEqual(response["Referrer-Policy"], "same-origin")
        self.assertIn("no-store", response["Cache-Control"])
        self.assertNotIn(self.secret, response["Location"])
        payload = self.payload()
        first = self.browser.post("/depot/version/", payload)
        self.assertEqual(first.status_code, 303)
        self.assertEqual(self.browser.post("/depot/version/", payload)["Location"], first["Location"])
        self.assertEqual(Submission.objects.count(), 1)
        receipt = self.browser.get(first["Location"])
        self.assertContains(receipt, "Version reçue")
        self.assertContains(receipt, "Version 1")
        self.assertNotContains(receipt, payload["figma_url"])
        self.assertNotContains(receipt, "Client privé")
        services.revoke_invitation(self.manager, self.site.pk, self.invitation.pk)
        self.assertContains(self.browser.get(first["Location"]), "Invitation indisponible", status_code=404)
        self.assertContains(self.browser.post("/depot/version/", payload), "Invitation indisponible", status_code=404)
        self.assertEqual(Submission.objects.count(), 1)

    def test_field_error_preserves_text_and_targets_the_field(self):
        self.exchange(self.secret)
        payload = self.payload()
        payload.update(figma_url="https://example.invalid/design/non", comment="Un essai de couleur")
        response = self.browser.post("/depot/version/", payload)
        self.assertContains(response, "Un essai de couleur", status_code=422)
        self.assertContains(response, 'aria-invalid="true"', status_code=422)
        self.assertContains(response, 'id="url-error"', status_code=422)
        self.assertEqual(response.context["request_id"], payload["request_id"])
        self.assertFalse(Submission.objects.exists())

    def test_second_invitation_in_another_tab_cannot_receive_first_tabs_submission(self):
        self.exchange(self.secret)
        original = self.payload()
        other = Site.objects.create(client=self.site.client, name="Autre site")
        SiteGrant.objects.create(site=other, user=self.manager, level="manage")
        _, new_secret = services.create_invitation(self.manager, other.pk)
        self.exchange(new_secret)
        response = self.browser.post("/depot/version/", original)
        self.assertEqual(response.status_code, 409)
        self.assertFalse(Submission.objects.exists())

    def test_ineligible_codes_present_same_public_message_without_console_data(self):
        services.revoke_invitation(self.manager, self.site.pk, self.invitation.pk)
        expired, expired_secret = services.create_invitation(self.manager, self.site.pk)
        type(expired).objects.filter(pk=expired.pk).update(expires_at=timezone.now())
        for code in [self.secret, expired_secret, "indisponible"]:
            response = self.exchange(code)
            self.assertContains(response, "Invitation indisponible", status_code=404)
            self.assertNotContains(response, self.site.name, status_code=404)
            self.assertNotContains(response, self.site.client.display_name, status_code=404)
            if code != "indisponible":
                self.assertNotContains(response, code, status_code=404)

    def test_missing_receipt_preserves_ability_to_submit_and_contains_no_private_data(self):
        self.exchange(self.secret)
        response = self.browser.get(f"/depot/recu/{uuid4()}/")
        self.assertContains(response, "Reçu indisponible", status_code=404)
        self.assertIn("no-store", response["Cache-Control"])
        self.assertNotContains(response, self.site.name, status_code=404)
        self.payload()

    def test_limit_response_keeps_form_and_returns_retry_after(self):
        self.exchange(self.secret)
        for _ in range(5):
            self.assertEqual(self.browser.post("/depot/version/", self.payload()).status_code, 303)
        payload = self.payload()
        payload["comment"] = "Proposition à garder"
        response = self.browser.post("/depot/version/", payload)
        self.assertContains(response, "Proposition à garder", status_code=429)
        self.assertGreater(int(response["Retry-After"]), 0)
        self.assertEqual(Submission.objects.count(), 5)

    def test_an_operator_session_alone_cannot_open_a_guest_form(self):
        self.browser.force_login(self.manager)
        self.assertEqual(self.browser.get("/depot/version/").status_code, 404)
        self.assertContains(self.browser.get("/depot/"), "Code d’invitation")
