from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from composition.editor import creer_atelier
from composition.models import CompositionRevision
from registre.models import Client, Site, SiteGrant
from workspace.access import OPERATOR_GROUP


class BuilderParityTests(TestCase):
    def setUp(self):
        self.operator = User.objects.create_user("atelier-parite")
        self.operator.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        self.site = Site.objects.create(name="Témoin", client=Client.objects.create(
            display_name="Atelier", client_type="COMPANY"))
        self.grant = SiteGrant.objects.create(site=self.site, user=self.operator, level="manage")
        self.client.force_login(self.operator)
        self.entry = reverse("registre:site-builder", args=[self.site.pk])
        self.base = creer_atelier(self.operator, self.site.pk, "template")
        self.page = self.base["document"]["pages"][0]
        self.section = self.page["sections"][0]

    def test_bookmark_and_read_only_section(self):
        params = {"page": self.page["id"], "selection": self.section["id"], "edit": "1"}
        for width, fmt in ((320, "mobile"), (767, "mobile"), (768, "tablet"),
                           (1023, "tablet"), (1024, "base"), (1920, "base")):
            with self.subTest(width=width):
                data = self.client.get(self.entry, {**params, "largeur": width}).context["builder_edit"]
                self.assertEqual((data["width"], data["format"], data["selection"], data["open_editor"]),
                                 (width, fmt, self.section["id"], True))
        for width in (319, 1921, "NaN"):
            self.assertEqual(self.client.get(self.entry, {**params, "largeur": width}).status_code, 404)
        self.grant.level = "read"
        self.grant.save()
        response = self.client.get(self.entry, {**params, "mode": "structure", "format": "tablet"})
        self.assertContains(response, "Section sélectionnée")
        self.assertContains(response, 'data-width="820"')
        self.assertContains(response, "Articles Wagtail de la page")
        self.assertNotContains(response, 'id="be-work"')
        missing = self.client.get(self.entry, {**params, "selection": uuid4()})
        self.assertContains(missing, "La sélection demandée est absente")
        self.assertEqual(CompositionRevision.objects.filter(site=self.site).count(), 1)

    def test_order_identity_flow_sizes_and_inheritance_on_save(self):
        local = str(uuid4())
        existing = self.section["id"]
        block = self.section["blocks"][0]["id"]
        commands = [
            {"action": "section_add", "local_id": local, "before": existing},
            {"action": "section_move", "id": existing, "before": local},
            {"action": "block_place", "id": block, "format": "base", "patch": {"width": 80}},
            {"action": "block_place", "id": block, "format": "mobile", "patch": {"width": 55, "height": 100}},
            {"action": "block_place", "id": block, "format": "mobile", "patch": {}, "clear": ["width"]},
            {"action": "section_remove", "id": local, "confirmed": True},
        ]
        response = self.client.post(reverse("registre:builder-save", args=[self.site.pk]), {
            "base": self.base["id"], "page": self.page["id"], "key": str(uuid4()),
            "commands": commands, "selection": block,
        }, content_type="application/json")
        self.assertEqual(response.status_code, 200, response.content)
        saved = CompositionRevision.objects.get(pk=response.json()["revision"])
        sections = saved.document["pages"][0]["sections"]
        self.assertEqual([s["id"] for s in sections], [existing])
        self.assertEqual(sections[0]["blocks"][0]["placement"], {"base": {"width": 80}, "mobile": {"height": 100}})
        self.assertEqual(response.json()["selection"], block)
        self.assertEqual(CompositionRevision.objects.get(pk=self.base["id"]).document, self.base["document"])
