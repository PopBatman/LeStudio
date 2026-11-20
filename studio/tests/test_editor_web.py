from django.contrib.auth.models import Group, User
from django.test import Client as WebClient

from composition.models import ComponentVersion
from composition.services import lire_brouillon
from registre.models import Client, Site, SiteGrant
from tests.catalogue_fixture import CatalogueTestCase
from workspace.access import OPERATOR_GROUP


class EditorWebTests(CatalogueTestCase):
    def setUp(self):
        self.actor = User.objects.create_user("gestion")
        self.actor.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        owner = Client.objects.create(display_name="Client test", client_type="COMPANY")
        self.site = Site.objects.create(client=owner, name="Atelier test")
        self.grant = SiteGrant.objects.create(user=self.actor, site=self.site, level="manage")
        self.client.force_login(self.actor)
        self.url = f"/sites/{self.site.pk}/atelier/"

    def head(self):
        return lire_brouillon(self.actor, self.site.pk)

    def create(self, origin):
        response = self.client.post(self.url, {"action": "create", "origin": origin})
        self.assertEqual(response.status_code, 302)
        return self.head()["document"]["pages"][0]

    def test_creation_choices_and_permissions(self):
        self.assertContains(self.client.get(self.url), "Figma")
        self.assertEqual(self.client.post(self.url, {"action": "create", "origin": "figma"}).status_code, 422)
        self.assertIsNone(self.head())
        guarded = WebClient(enforce_csrf_checks=True)
        guarded.force_login(self.actor)
        self.assertEqual(guarded.post(self.url, {"action": "create", "origin": "blank"}).status_code, 403)
        page = self.create("blank")
        self.assertEqual(page["sections"], [])
        local = self.head()["id"]
        self.assertContains(self.client.get(self.url), "Accueil")
        self.assertEqual(self.client.post(self.url, {"action": "create", "origin": "blank"}).status_code, 409)
        self.grant.level = "read"
        self.grant.save()
        self.assertContains(self.client.get(self.url), "Accueil")
        self.assertEqual(self.client.post(self.url, {"action": "section_add"}).status_code, 403)
        self.assertEqual(self.head()["id"], local)
        self.grant.delete()
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_template_edit_move_and_reload(self):
        page = self.create("template")
        section = page["sections"][0]
        title, text = section["blocks"]
        selection = {"page": page["id"], "section": section["id"], "node": title["id"]}
        def post(action, **fields):
            return self.client.post(self.url, {**selection, "base": self.head()["id"], "action": action, **fields})
        self.assertEqual(post("block_edit", prop_level=2, prop_text="Nouveau titre").status_code, 302)
        container = ComponentVersion.objects.get(site=None, key="container", version=1)
        self.assertEqual(post("block_add", definition=container.pk, parent=section["id"]).status_code, 302)
        parent = self.head()["document"]["pages"][0]["sections"][0]["blocks"][-1]
        self.assertEqual(post("block_move", node=text["id"], parent=parent["id"]).status_code, 302)
        self.assertEqual(post("block_move", node=parent["id"], parent=section["id"], before=title["id"]).status_code, 302)
        blocks = self.head()["document"]["pages"][0]["sections"][0]["blocks"]
        self.assertEqual([b["id"] for b in blocks], [parent["id"], title["id"]])
        self.assertEqual(blocks[0]["children"][0]["id"], text["id"])
        self.assertContains(self.client.get(self.url, selection), "Nouveau titre")
        self.assertEqual(self.client.get(self.url, {**selection, "node": str(self.site.pk)}).status_code, 404)

    def test_invalid_fields_and_stale_proposal_when_target_disappears(self):
        page = self.create("template")
        section = page["sections"][0]
        node = section["blocks"][0]
        data = {"page": page["id"], "section": section["id"], "node": node["id"], "base": self.head()["id"]}
        bad = self.client.post(self.url, {**data, "action": "block_edit", "prop_text": "À garder", "prop_level": 8})
        self.assertContains(bad, "À garder", status_code=422)
        self.assertEqual(self.head()["id"], data["base"])
        self.assertEqual(self.client.post(self.url, {**data, "action": "block_remove", "confirmed": "on"}).status_code, 302)
        local = self.head()["id"]
        proposal = {**data, "action": "block_edit", "prop_text": "Proposition conservée", "prop_level": 2}
        for extra in ({}, {"relire": "1"}):
            response = self.client.post(self.url, {**proposal, **extra})
            self.assertContains(response, "Proposition conservée", status_code=409)
        self.assertEqual(self.head()["id"], local)

    def test_conflict_requires_comparison_then_fresh_post(self):
        page = self.create("template")
        section = page["sections"][0]
        data = {"action": "block_edit", "page": page["id"], "section": section["id"],
                "node": section["blocks"][0]["id"], "base": self.head()["id"], "prop_level": 1}
        self.assertEqual(self.client.post(self.url, {**data, "prop_text": "Titre courant"}).status_code, 302)
        proposal = {**data, "prop_text": "Titre proposé"}
        conflict = self.client.post(self.url, proposal)
        self.assertContains(conflict, "Titre courant", status_code=409)
        self.assertContains(conflict, "Titre proposé", status_code=409)
        local = self.head()["id"]
        compared = self.client.post(self.url, {**proposal, "relire": "1"})
        self.assertContains(compared, local)
        self.assertEqual(self.head()["id"], local)
        self.assertEqual(self.client.post(self.url, {**proposal, "base": local}).status_code, 302)

    def test_sections_keyboard_placement_and_cancel_without_mutation(self):
        page = self.create("blank")
        selection = {"page": page["id"], "action": "section_add"}
        def save(**fields):
            return self.client.post(self.url, {**selection, "display": "stack", "base": self.head()["id"], **fields})
        self.assertEqual(save().status_code, 302)
        first = self.head()["document"]["pages"][0]["sections"][0]["id"]
        self.assertEqual(save(before=first).status_code, 302)
        second = self.head()["document"]["pages"][0]["sections"][0]["id"]
        self.assertNotEqual(first, second)
        self.assertEqual(save(action="section_move", section=first, before=second).status_code, 302)
        local = self.head()
        self.assertEqual([s["id"] for s in local["document"]["pages"][0]["sections"]], [first, second])
        self.assertContains(self.client.get(self.url, {**selection, "section": first, "action": "section_remove"}),
                            "Annuler")
        self.assertEqual(save(action="section_remove", section=first).status_code, 422)
        self.assertEqual(self.head()["id"], local["id"])
        self.assertEqual(save(action="section_remove", section=first, confirmed="on").status_code, 302)

    def test_foreign_site_revision_and_selection_are_opaque(self):
        from composition.editor import creer_atelier

        page = self.create("template")
        other = Site.objects.create(client=self.site.client, name="Site confidentiel")
        grant = SiteGrant.objects.create(user=self.actor, site=other, level="manage")
        foreign = creer_atelier(self.actor, other.pk, "template")
        grant.delete()
        local = self.head()["id"]
        for params in ({"page": foreign["document"]["pages"][0]["id"]},
                       {"page": page["id"], "section": foreign["document"]["pages"][0]["sections"][0]["id"]}):
            self.assertNotContains(self.client.get(self.url, params), other.name, status_code=404)
        self.assertEqual(self.client.post(self.url, {"page": page["id"], "action": "section_add",
                         "base": foreign["id"], "display": "stack"}).status_code, 404)
        self.assertEqual(self.head()["id"], local)

    def test_historical_opaque_properties_remain_readable(self):
        from uuid import uuid4
        from composition.services import creer_brouillon

        page_id, section_id, node_id = [str(uuid4()) for _ in range(3)]
        block = {"id": node_id, "definition": {"scope": "site", "key": "archives", "version": 1},
                 "props": {"layout": "Disposition historique", "media": "Ancienne légende"}, "children": []}
        document = {"schema_version": 1, "theme": {}, "menus": [], "pages": [{"id": page_id, "parent_id": None,
                    "slug": "", "title": "Archives", "sections": [{"id": section_id,
                    "layout": {"base": {}}, "blocks": [block]}]}]}
        initial = creer_brouillon(self.actor, self.site.pk, {"kind": "blank"}, document,
                                  resolve_definition=lambda *args: {"layout": "text", "media": "text"})
        response = self.client.get(self.url, {"page": page_id, "section": section_id, "node": node_id})
        self.assertContains(response, "Disposition historique")
        self.assertContains(response, "Ancienne légende")
        self.assertEqual(self.head()["id"], initial["id"])

    def test_pinned_retired_version_and_invalid_button_url(self):
        page = self.create("template")
        section = page["sections"][0]
        heading = ComponentVersion.objects.get(site=None, key="heading", version=1)
        ComponentVersion.objects.filter(pk=heading.pk).update(retired=True)
        data = {"page": page["id"], "section": section["id"], "node": section["blocks"][0]["id"],
                "action": "block_edit", "definition": heading.pk, "base": self.head()["id"]}
        self.assertEqual(self.client.post(self.url, {**data, "prop_text": "Titre conservé", "prop_level": 1}).status_code, 302)
        current = self.head()["id"]
        button = ComponentVersion.objects.get(site=None, key="button", version=1)
        bad = self.client.post(self.url, {**data, "action": "block_add", "base": current,
                               "parent": section["id"], "definition": button.pk, "prop_label": "En savoir plus",
                               "prop_url": "https://["})
        self.assertContains(bad, "HTTPS complète", status_code=422)
        self.assertEqual(self.head()["id"], current)

    def test_stale_edit_follows_same_occurrence_moved_to_another_section(self):
        page = self.create("template")
        first = page["sections"][0]
        node = first["blocks"][1]
        self.client.post(self.url, {"action": "section_add", "page": page["id"],
                                    "base": self.head()["id"], "display": "stack"})
        head = self.head()
        last = head["document"]["pages"][0]["sections"][1]
        data = {"page": page["id"], "section": first["id"], "node": node["id"], "base": head["id"]}
        self.assertEqual(self.client.post(self.url, {**data, "action": "block_move",
                                                     "parent": last["id"]}).status_code, 302)
        proposal = {**data, "action": "block_edit", "prop_text": "Texte rapproché"}
        self.assertContains(self.client.post(self.url, proposal), "Relire la révision courante", status_code=409)
        response = self.client.post(self.url, {**proposal, "relire": 1})
        self.assertContains(response, f'name="section" value="{last["id"]}"')
        self.assertEqual(self.client.post(self.url, {**proposal, "section": last["id"],
                                                     "base": self.head()["id"]}).status_code, 302)
