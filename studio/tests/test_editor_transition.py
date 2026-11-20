from copy import deepcopy
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import TestCase, override_settings
from django.urls import reverse

from composition.catalogue import installer_version
from composition.models import ComponentVersion, CompositionRevision
from registre.models import Client, Site, SiteGrant
from workspace.access import OPERATOR_GROUP
from .test_composition_services import sample_document


class EditorTransitionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("transition")
        self.user.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        owner = Client.objects.create(display_name="Recette", client_type="COMPANY")
        self.site = Site.objects.create(client=owner, name="Recette")
        self.other = Site.objects.create(client=owner, name="Autre")
        self.grant = SiteGrant.objects.create(site=self.site, user=self.user, level="manage")
        self.client.force_login(self.user)

    def url(self, name):
        return reverse("registre:" + name, args=[self.site.pk])

    def revision(self, schema=1):
        doc = sample_document()
        doc["schema_version"] = schema
        if schema >= 2:
            doc["menus"] = [{"id":str(uuid4()),"label":"Principal","items":[{
                "id":str(uuid4()),"parent_id":None,"label":"Ateliers","visibility":["mobile"],
                "target":{"kind":"page","page_id":doc["pages"][1]["id"]}}]}]
        if schema >= 3:
            doc["theme"] = {"gap":12,"font":"dm-sans"}
            version = installer_version(self.site, "legende", 1, "Légende du site", "text")
            ComponentVersion.objects.filter(pk=version.pk).update(retired=True)
            sibling = doc["pages"][0]["sections"][0]["blocks"][1]
            sibling["definition"] = {"scope":"site","key":"legende","version":1}
            sibling["appearance"] = {"tokens":{"gap":8}}
        if schema >= 4:
            sibling["placement"] = {"base":{"mode":"free","x":10,"width":60,"y":16,"height":112,"z":2},
                                    "mobile":{"mode":"flow"}}
        return CompositionRevision.objects.create(site=self.site, document=doc, number=1,
                                                  origin={"kind": "blank"}, author=self.user)

    def test_navigation_modes(self):
        for mode in ("coexistence", "builder", "compatibility"):
            with self.subTest(mode=mode), override_settings(STUDIO_EDITOR_MODE=mode):
                html = self.client.get(self.url("site"))
                route = "site-editor" if mode == "coexistence" else "site-builder"
                self.assertContains(html, f'class="btn btn-primary" href="{self.url(route)}"')
                response = self.client.get(self.url("site-editor"))
                self.assertEqual(response.status_code, 302 if mode == "compatibility" else 200)

    @override_settings(STUDIO_EDITOR_MODE="compatibility")
    def test_bookmark_and_stale_form(self):
        rev = self.revision()
        page = rev.document["pages"][0]
        section = page["sections"][0]
        node = section["blocks"][0]["id"]
        data = dict(revision=str(rev.pk), page=page["id"], section=section["id"], node=node,
                    format="mobile", largeur="455")
        old = self.url("site-canvas")
        target = urlsplit(self.client.get(old, data).url)
        self.assertEqual(target.path, self.url("site-builder"))
        self.assertEqual(parse_qs(target.query), {k:[v] for k,v in dict(
            revision=str(rev.pk),page=page["id"],selection=node,format="mobile",largeur="455").items()})
        self.assertContains(self.client.post(old, data), "Relire", status_code=409)
        self.assertContains(self.client.get(old, {**data,"node":str(uuid4())}), "introuvable")
        self.assertEqual(self.client.get(old, {"revision":str(uuid4())}).status_code,404)
        self.grant.level = "read"
        self.grant.save()
        self.assertEqual(self.client.post(old, data).status_code,403)
        self.assertEqual(self.client.get(old, {**data,"action":"block_edit"}).status_code,403)
        self.assertEqual(self.client.get(old, data).status_code,302)
        foreign = reverse("registre:site-canvas", args=[self.other.pk])
        self.assertEqual(self.client.get(foreign).status_code,404)
        self.assertEqual(self.client.post(foreign).status_code,404)
        self.assertEqual(CompositionRevision.objects.count(),1)

    def test_schema_roundtrip_and_replayed_save(self):
        for schema in (1,2,3,4):
            with self.subTest(schema=schema):
                rev = self.revision(schema)
                original = deepcopy(rev.document)
                page = original["pages"][0]
                node = page["sections"][0]["blocks"][0]
                with override_settings(STUDIO_EDITOR_MODE="builder"):
                    packet = {"base":str(rev.pk),"page":page["id"],"key":str(uuid4()),
                              "commands":[{"action":"block_edit","id":node["id"],"definition":node["definition"],
                                           "props":{"text":"Après bascule"}}]}
                    saved = self.client.post(self.url("builder-save"),packet,content_type="application/json")
                    self.assertEqual(saved.status_code,200,saved.content)
                    retry = self.client.post(self.url("builder-save"),packet,content_type="application/json")
                    self.assertEqual(saved.json(),retry.json())
                    conflict = self.client.post(self.url("builder-save"),{**packet,"key":str(uuid4())},
                                                content_type="application/json")
                    self.assertEqual(conflict.status_code,409)
                with override_settings(STUDIO_EDITOR_MODE="coexistence"):
                    self.assertContains(self.client.get(self.url("site-editor")), "Après bascule")
                    rev.refresh_from_db()
                    self.assertEqual(rev.document,original)
                    head = CompositionRevision.objects.get(parent=rev)
                    self.assertEqual(head.number,2)
                    expected = deepcopy(original)
                    expected["schema_version"] = head.document["schema_version"]
                    expected["pages"][0]["sections"][0]["blocks"][0]["props"]["text"] = "Après bascule"
                    self.assertEqual(head.document, expected)
                    stale_form = {"base":str(rev.pk),"page":page["id"],"section":page["sections"][0]["id"],
                                  "node":node["id"],"action":"block_edit","prop_text":"Autre saisie"}
                    self.assertContains(self.client.post(self.url("site-editor"),stale_form),
                                        "Autre saisie",status_code=409)
                    self.assertEqual(CompositionRevision.objects.filter(site=self.site).count(),2)
                self.site = Site.objects.create(client=self.site.client,name=f"Suite {schema}")
                SiteGrant.objects.create(site=self.site,user=self.user,level="manage")
