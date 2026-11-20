from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import Client as WebClient, TestCase

from composition.models import CompositionRevision
from composition.services import lire_brouillon
from registre.models import Client, Site, SiteGrant
from workspace.access import OPERATOR_GROUP


class NavigationWebTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("gestion")
        self.user.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        owner = Client.objects.create(display_name="Maison fictive", client_type="COMPANY")
        self.site = Site.objects.create(client=owner, name="Maison des dunes")
        self.grant = SiteGrant.objects.create(user=self.user, site=self.site, level="manage")
        self.client.force_login(self.user)
        self.base = f"/sites/{self.site.pk}/"
        self.pages, self.menus = self.base + "pages/", self.base + "menus/"

    def head(self):
        return lire_brouillon(self.user, self.site.pk)

    def edit(self, endpoint, action, **values):
        return self.client.post(endpoint, {"action": action, "base": self.head()["id"], **values})

    def create(self):
        self.assertEqual(self.client.post(self.pages, {"action": "blank"}).status_code, 302)
        return self.head()["document"]["pages"][0]["id"]

    def test_entry_empty_permissions_and_csrf(self):
        self.assertContains(self.client.get(self.base), self.pages)
        self.assertContains(self.client.get(self.pages), "Créer un brouillon vierge")
        self.assertFalse(CompositionRevision.objects.exists())
        csrf = WebClient(enforce_csrf_checks=True)
        csrf.force_login(self.user)
        self.assertEqual(csrf.post(self.pages, {"action": "blank"}).status_code, 403)
        self.grant.level = "read"
        self.grant.save()
        self.assertNotContains(self.client.get(self.pages), "Créer un brouillon vierge")
        self.assertEqual(self.client.post(self.menus, {"action": "blank"}).status_code, 403)
        self.grant.delete()
        self.assertEqual(self.client.get(self.menus).status_code, 404)
        self.assertEqual(self.client.post(self.pages, {"action": "blank"}).status_code, 404)
        self.assertFalse(CompositionRevision.objects.exists())

    def test_create_link_review_delete_and_preserve_candidate_on_conflict(self):
        root = self.create()
        self.assertEqual(self.edit(self.pages, "page_add", title="Carnet", slug="carnet", parent_id=root).status_code, 302)
        page = self.head()["document"]["pages"][-1]["id"]
        self.assertContains(self.client.get(self.pages, {"selection": page}), "Hors menu")
        self.assertEqual(self.edit(self.menus, "menu_add", label="Principal").status_code, 302)
        menu = self.head()["document"]["menus"][0]["id"]
        entry = {"menu_id": menu, "label": "Visiter", "kind": "page", "page_id": page,
                 "visibility": ["desktop", "tablet", "mobile"]}
        self.assertEqual(self.edit(self.menus, "item_add", **entry).status_code, 302)
        item = self.head()["document"]["menus"][0]["items"][0]["id"]
        stale = self.head()["id"]
        rename = {"id": page, "title": "Carnet", "slug": "journal"}
        impact = self.edit(self.pages, "page_edit", **rename)
        self.assertContains(impact, "/journal/")
        self.assertContains(impact, "Visiter")
        token = impact.context["impact"]["token"]
        self.assertEqual(self.head()["id"], stale)
        self.assertEqual(self.edit(self.pages, "page_edit", confirmation=token, **rename).status_code, 302)
        conflict = self.client.post(self.pages, {"action": "page_edit", "base": stale, "id": page,
                                                  "title": "Autre proposition", "slug": "essai"})
        self.assertContains(conflict, "Autre proposition", status_code=409)
        self.assertContains(conflict, "Relire la révision courante", status_code=409)
        self.assertContains(self.edit(self.pages, "page_delete", id=page), "Visiter")
        resolution = {"resolution_" + item: root}
        review = self.edit(self.pages, "page_delete", id=page, **resolution)
        self.assertTrue(review.context["impact"]["complete"])
        self.assertContains(review, f'name="resolution_{item}"')
        self.assertContains(review, f'value="{root}" selected')
        earlier = self.head()["id"]
        self.edit(self.pages, "page_edit", id=root, title="Accueil du site", slug="")
        submitted = {"action": "page_delete", "base": earlier, "id": page,
                     "confirmation": review.context["impact"]["token"], **resolution}
        conflict = self.client.post(self.pages, submitted)
        self.assertContains(conflict, "Décisions proposées", status_code=409)
        reloaded = self.client.post(self.pages, {**submitted, "relire": "1"})
        self.assertContains(reloaded, "Révision courante")
        self.assertContains(reloaded, "Visiter")
        self.assertNotContains(reloaded, f'name="resolution_{item}"')
        review = self.edit(self.pages, "page_delete", id=page, **resolution)
        self.assertEqual(self.edit(self.pages, "page_delete", id=page,
                                   confirmation=review.context["impact"]["token"], **resolution).status_code, 302)
        doc = self.head()["document"]
        self.assertEqual([p["id"] for p in doc["pages"]], [root])
        self.assertEqual(doc["menus"][0]["items"][0]["target"]["page_id"], root)
        self.assertContains(self.client.get(self.menus), "Visiter")
        self.assertEqual(self.client.get(self.menus, {"menu": uuid4()}).status_code, 404)

    def test_menu_visibility_inherits_parent_and_reorders_after_reload(self):
        root = self.create()
        self.edit(self.menus, "menu_add", label="Principal")
        menu = self.head()["document"]["menus"][0]["id"]
        for kind, name in (("group", "Découvrir"), ("page", "Accueil")):
            response = self.edit(self.menus, "item_add", menu_id=menu, kind=kind, label=name, page_id=root,
                                 visibility=["desktop"])
            self.assertEqual(response.status_code, 302)
        group, page = self.head()["document"]["menus"][0]["items"]
        self.edit(self.menus, "item_add", kind="external", label="Partenaire", url="https://example.org/",
                  menu_id=menu, parent_id=group["id"], visibility=["mobile"])
        self.assertContains(self.client.get(self.menus), "Masquée sur tous les formats")
        self.assertEqual(self.edit(self.menus, "item_move", menu_id=menu, id=page["id"],
                                   parent_id="", before_id=group["id"]).status_code, 302)
        items = self.client.get(self.menus).context["items"]
        self.assertEqual([i["label"] for i in items], ["Accueil", "Découvrir", "Partenaire"])
        self.assertEqual(self.edit(self.menus, "item_delete", id=group["id"], menu_id=menu).status_code, 422)
        proposal = dict(id=group["id"], menu_id=menu, branch="on")
        review = self.edit(self.menus, "item_delete", **proposal)
        self.assertContains(review, "Partenaire")
        self.assertEqual(self.edit(self.menus, "item_delete", confirmation=review.context["impact"]["token"],
                                   **proposal).status_code, 302)
        self.assertEqual(len(self.head()["document"]["menus"][0]["items"]), 1)
