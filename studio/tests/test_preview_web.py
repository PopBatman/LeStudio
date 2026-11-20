from datetime import timedelta
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import Client as Browser, TestCase
from django.utils import timezone

from composition.models import CompositionRevision, PreviewTicket
from composition.services import creer_brouillon
from registre.models import Client, Site, SiteGrant
from workspace.access import OPERATOR_GROUP


class PreviewWebTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("lectrice")
        self.user.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        owner = Client.objects.create(display_name="Atelier fictif", client_type="COMPANY")
        self.site = Site.objects.create(client=owner, name="Atelier des voiles")
        self.grant = SiteGrant.objects.create(user=self.user, site=self.site, level="manage")
        self.revision = creer_brouillon(self.user, self.site.pk, {"kind": "blank"})
        self.page = self.revision["document"]["pages"][0]["id"]
        self.grant.level = "read"
        self.grant.save()
        self.client.force_login(self.user)
        self.url = f"/sites/{self.site.pk}/apercu/"
        self.params = {"revision": self.revision["id"], "page": self.page}
        self.rendering = patch("composition.preview_views.render_preview").start()
        self.addCleanup(patch.stopall)
        self.rendering.return_value = {"html": "<p>Voiles</p>", "manifest": {
            "instance_id": str(uuid4()), "definitions": [], "articles": {}, "media": {},
        }}

    def prepare(self):
        response = self.client.post(self.url, self.params)
        self.assertEqual(response.status_code, 302)
        return response.url

    def test_session_scope_no_store_expiry_and_no_publication(self):
        before = CompositionRevision.objects.count()
        address = self.prepare()
        self.assertContains(self.client.get(address), "Version active inconnue")
        document = address + "document/"
        page = self.client.get(document)
        self.assertContains(page, "Voiles")
        self.assertIn("sandbox", page["Content-Security-Policy"])
        self.assertIn("no-store", page["Cache-Control"])
        other = Browser()
        other.force_login(self.user)
        self.assertEqual(other.get(document).status_code, 404)
        with patch("composition.preview_views.timezone.now", return_value=timezone.now()+timedelta(minutes=10)):
            self.assertEqual(self.client.get(document).status_code, 410)
        self.assertEqual(CompositionRevision.objects.count(), before)

    def test_changed_result_and_revoked_rights(self):
        address = self.prepare()
        self.rendering.return_value["html"] = "<p>Autre</p>"
        response = self.client.get(address + "document/")
        self.assertEqual(response.status_code, 409)
        self.assertNotIn(b"<p>Autre</p>", response.content)
        self.grant.delete()
        self.assertEqual(self.client.get(address).status_code, 404)
        self.assertEqual(self.client.get(address + "document/").status_code, 404)

    def test_close_and_csrf(self):
        browser = Browser(enforce_csrf_checks=True)
        browser.force_login(self.user)
        self.assertEqual(browser.post(self.url, self.params).status_code, 403)
        address = self.prepare()
        self.assertEqual(self.client.post(address + "fermer/").status_code, 302)
        self.assertFalse(PreviewTicket.objects.exists())
        self.assertEqual(self.client.get(address + "document/").status_code, 404)

    def test_newer_revision_can_be_compared_with_previous_page(self):
        from composition.services import modifier_navigation
        self.grant.level = "manage"
        self.grant.save()
        old = self.prepare()
        saved = modifier_navigation(self.user, self.site.pk, self.revision["id"], {
            "action": "page_edit", "id": self.page, "title": "Nos voiles", "slug": ""})
        self.assertContains(self.client.get(old), "Vous examinez toujours R1")
        self.params["revision"] = saved["id"]
        current = self.prepare()
        self.assertContains(self.client.get(current), "Titre de page modifié")
        self.assertContains(self.client.get(current), "Examiner la même page en R1")

    def test_logout_discards_receipts(self):
        self.prepare()
        self.client.logout()
        self.assertFalse(PreviewTicket.objects.exists())

    def test_secondary_page_return_and_missing_page_selection(self):
        from composition.services import modifier_navigation
        self.grant.level = "manage"
        self.grant.save()
        saved = modifier_navigation(self.user, self.site.pk, self.revision["id"], {
            "action": "page_add", "parent_id": self.page, "title": "Contact", "slug": "contact"})
        child = saved["document"]["pages"][-1]["id"]
        self.params.update(revision=saved["id"], page=child)
        address = self.prepare()
        response = self.client.post(address + "fermer/", {"origine": "canvas"})
        self.assertEqual(response.url, f"/sites/{self.site.pk}/atelier/canvas/?page={child}")
        earlier = self.client.get(self.url, {"page": child, "revision": self.revision["id"]})
        self.assertContains(earlier, "La page demandée est absente")
        self.assertContains(earlier, '<option value="" selected disabled>Choisir une page</option>', html=True)
