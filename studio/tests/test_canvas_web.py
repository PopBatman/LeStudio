from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import Client as HttpClient

from composition.editor import creer_atelier
from composition.services import lire_brouillon
from registre.models import Client, Site, SiteGrant
from tests.catalogue_fixture import CatalogueTestCase
from workspace.access import OPERATOR_GROUP


class CanvasWebTests(CatalogueTestCase):
    def setUp(self):
        self.actor = User.objects.create_user("atelier-test")
        self.actor.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        owner = Client.objects.create(display_name="Client fictif", client_type="COMPANY")
        self.site = Site.objects.create(client=owner, name="Atelier fictif")
        self.grant = SiteGrant.objects.create(user=self.actor, site=self.site, level="manage")
        self.client.force_login(self.actor)
        self.editor = f"/sites/{self.site.pk}/atelier/"
        self.url = self.editor + "canvas/"
        self.head = creer_atelier(self.actor, self.site.pk, "template")
        page = self.head["document"]["pages"][0]
        section = page["sections"][0]
        self.sel = {"page": page["id"], "section": section["id"], "node": section["blocks"][0]["id"]}
        self.place = {**self.sel, "action": "block_place", "base": self.head["id"]}

    def current(self):
        return lire_brouillon(self.actor, self.site.pk)

    def test_shared_selection_and_breakpoints(self):
        self.assertContains(self.client.get(self.editor, self.sel), self.url)
        for width, fmt in [(767,"mobile"), (768,"tablet"), (1023,"tablet"), (1024,"base")]:
            response = self.client.get(self.url, {**self.sel, "largeur": width})
            self.assertEqual(response.context["format"], fmt)
            self.assertEqual(response.context["canvas_width"], width)
            self.assertEqual(response.context["node_id"], self.sel["node"])
        self.assertEqual(self.client.get(self.url, {**self.sel, "node": uuid4()}).status_code, 404)

    def test_place_then_read_and_clear_in_structure(self):
        free = {"mode":"free", "x":10,"width":65,"y":15,"height":110,"z":1}
        response = self.client.post(self.url, {**self.place, **free})
        self.assertEqual(response.status_code, 302)
        current = self.current()
        placed = self.client.get(self.url, self.sel).context["canvas_sections"][0]["items"][0]
        self.assertEqual(placed["placement"]["width"], 65)
        tablet = {**self.place,"format":"tablet","base":current["id"]}
        self.assertEqual(self.client.post(self.editor, {**tablet, "width":50, "z":5}).status_code,302)
        self.assertEqual(self.client.post(self.url, {**tablet,"base":self.current()["id"],"clear":"width"}).status_code,302)
        self.assertEqual(self.current()["document"]["pages"][0]["sections"][0]["blocks"][0]["placement"]["tablet"],{"z":5})

    def test_readonly_csrf_invalid_and_cross_view_conflict(self):
        guarded = HttpClient(enforce_csrf_checks=True)
        guarded.force_login(self.actor)
        self.assertEqual(guarded.post(self.url,self.place).status_code,403)
        self.assertEqual(self.client.post(self.url,{**self.place,"width":101}).status_code,422)
        self.assertEqual(self.current()["id"], self.head["id"])
        self.assertEqual(self.client.post(self.editor,{**self.place,"width":70}).status_code,302)
        proposed = {**self.place,"width":85}
        self.assertContains(self.client.post(self.url,proposed),"85",status_code=409)
        rev = self.current()["id"]
        self.assertContains(self.client.post(self.url,{**proposed,"relire":1}),rev)
        self.assertEqual(self.current()["id"],rev)
        self.grant.level="read"; self.grant.save()
        self.assertContains(self.client.get(self.url,self.sel),"Lecture seule")
        self.assertEqual(self.client.post(self.url,proposed).status_code,403)
        self.grant.delete()
        self.assertEqual(self.client.get(self.url).status_code,404)

    def test_layout_and_overflow_are_bound_to_the_selected_format(self):
        layout = {**self.sel, "node":"", "format":"tablet", "action":"parent_layout",
                  "base":self.current()["id"], "display":"grid", "columns":3}
        self.assertEqual(self.client.post(self.url, layout).status_code, 302)
        section = self.current()["document"]["pages"][0]["sections"][0]
        self.assertEqual(section["layout"]["tablet"], {"display":"grid","columns":3})
        state = self.current()["id"]
        overflow = {**self.place,"base":state,"format":"mobile","mode":"free","x":90,"width":30,
                    "y":0,"height":100}
        response = self.client.post(self.url, overflow)
        self.assertContains(response, "100 % du parent", status_code=422)
        self.assertIn("width", response.context["form"].errors)
        self.assertEqual(response.context["form"]["width"].value(), "30")
        self.assertEqual(self.current()["id"], state)
        other = {**self.place, "base":state, "parent":str(uuid4()), "width":60}
        self.assertEqual(self.client.post(self.url,other).status_code,422)
        self.assertEqual(self.current()["id"],state)

    def test_archived_layout_with_new_container_definition_stays_readable(self):
        from composition.catalogue import installer_version
        from composition.services import creer_brouillon

        site = Site.objects.create(client=self.site.client, name="Anciennes pages")
        SiteGrant.objects.create(user=self.actor, site=site, level="manage")
        page, section, block = (str(uuid4()) for _ in range(3))
        occurrence = {"id":block,"definition":{"scope":"site","key":"archives","version":1},
                      "props":{"layout":"Disposition historique"},"children":[]}
        original = {"schema_version":1,"theme":{},"menus":[],"pages":[{
            "id":page,"parent_id":None,"slug":"","title":"Archives","sections":[{
                "id":section,"layout":{"base":{}},"blocks":[occurrence]}]}]}
        rev = creer_brouillon(self.actor,site.pk,{"kind":"blank"},original,
                               resolve_definition=lambda *args:{"layout":"text"})
        installer_version(site,"archives",1,"Archives","container")
        url = f"/sites/{site.pk}/atelier/canvas/"
        selection = {"page":page,"section":section,"node":block}
        self.assertEqual(self.client.get(url).status_code,200)
        selected = self.client.get(url,selection)
        self.assertContains(selected,"Disposition historique")
        self.assertNotContains(selected,"Disposition responsive")
        for path in (url, f"/sites/{site.pk}/atelier/"):
            action = {**selection, "action":"parent_layout"}
            self.assertEqual(self.client.get(path,action).status_code,404)
            self.assertEqual(self.client.post(path,{**action,"base":rev["id"],"gap":10}).status_code,404)
        self.assertEqual(lire_brouillon(self.actor,site.pk)["id"],rev["id"])
