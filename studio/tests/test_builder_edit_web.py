import json
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import Client as Browser, TestCase
from django.urls import reverse

from composition.editor import creer_atelier
from composition.models import CompositionRevision
from registre.models import Client, Site, SiteGrant
from workspace.access import OPERATOR_GROUP


class BuilderEditWebTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("gestion-canvas")
        self.user.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        client = Client.objects.create(display_name="Atelier fictif", client_type="COMPANY")
        self.site = Site.objects.create(client=client, name="Gestion")
        self.grant = SiteGrant.objects.create(user=self.user, site=self.site, level="manage")
        self.entry = reverse("registre:site-builder", args=[self.site.pk])
        self.save = self.entry + "enregistrer/"
        self.client.force_login(self.user)

    def test_blank_start_head_catalogue_and_readonly(self):
        self.client.post(self.entry, {"start": "blank"})
        self.assertEqual(CompositionRevision.objects.filter(site=self.site).count(), 1)
        page = self.client.get(self.entry)
        self.assertTrue(page.context["builder_edit"]["definitions"])
        self.assertContains(page, "Modifier la page")
        self.client.post(self.entry, {"start": "blank"})
        self.assertEqual(CompositionRevision.objects.filter(site=self.site).count(), 1)
        self.grant.level = "read"
        self.grant.save()
        self.assertIsNone(self.client.get(self.entry).context.get("builder_edit"))
        self.assertEqual(self.client.head(self.save).status_code, 403)
        self.grant.delete()
        self.assertEqual(self.client.head(self.save).status_code, 404)

    def test_batch_retry_conflict_and_historical_shell(self):
        rev = creer_atelier(self.user, self.site.pk, "blank")
        payload = {"base": rev["id"], "page": rev["document"]["pages"][0]["id"],
                   "key": str(uuid4()), "commands": [{"action": "section_add", "local_id": str(uuid4())}]}
        def send():
            return self.client.post(self.save, json.dumps(payload), content_type="application/json")
        first = send()
        self.assertEqual(first.status_code, 200, first.content)
        self.assertEqual(first.json()["number"], 2)
        self.assertEqual(send().json(), first.json())
        payload["key"] = str(uuid4())
        self.assertEqual(send().status_code, 409)
        self.assertIsNone(self.client.get(self.entry, {"revision": rev["id"]}).context.get("builder_edit"))
        self.assertEqual(CompositionRevision.objects.filter(site=self.site).count(), 2)

    def test_csrf_method_and_body_validation(self):
        csrf = Browser(enforce_csrf_checks=True)
        csrf.force_login(self.user)
        self.assertEqual(csrf.post(self.save, "{}", content_type="application/json").status_code, 403)
        self.assertEqual(self.client.get(self.save).status_code, 405)
        self.assertEqual(self.client.head(self.save).status_code, 204)
        self.assertEqual(self.client.post(self.save, {"hello": "world"}).status_code, 415)
        for invalid in ("[", "null", "[]"):
            self.assertEqual(self.client.post(self.save, invalid, content_type="application/json").status_code, 400)
