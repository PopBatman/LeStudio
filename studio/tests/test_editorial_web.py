from django.contrib.auth.models import Group, User
from django.test import Client as HttpClient

from composition.editor import creer_atelier
from composition.services import lire_brouillon
from registre.models import Client, Site, SiteGrant
from tests.catalogue_fixture import CatalogueTestCase
from workspace.access import OPERATOR_GROUP


class EditorialWebTests(CatalogueTestCase):
    def setUp(self):
        self.actor = User.objects.create_user("redaction")
        self.actor.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        owner = Client.objects.create(display_name="Exemple", client_type="COMPANY")
        self.site = Site.objects.create(client=owner, name="Éditorial")
        self.grant = SiteGrant.objects.create(user=self.actor, site=self.site, level="manage")
        self.client.force_login(self.actor)
        self.url = f"/sites/{self.site.pk}/atelier/"
        self.head = creer_atelier(self.actor, self.site.pk, "template")
        page = self.head["document"]["pages"][0]
        self.selection = {"page": page["id"], "section": page["sections"][0]["id"]}
        self.action = {**self.selection, "action": "article_reference", "base": self.head["id"]}

    def test_section_offers_editorial_reference_and_labels_local_fields(self):
        for path in (self.url, self.url + "canvas/"):
            self.assertContains(self.client.get(path, self.selection), "Associer un article Wagtail")
            self.assertContains(self.client.get(path, self.action), "Identifiant de la page Wagtail")
            node = self.head["document"]["pages"][0]["sections"][0]["blocks"][0]["id"]
            self.assertContains(self.client.get(path, {**self.selection, "node": node}), "Édité dans Studio")
            self.assertEqual(self.client.get(path, {**self.action, "node": node}).status_code, 404)

    def test_permissions_csrf_and_validation(self):
        guarded = HttpClient(enforce_csrf_checks=True)
        guarded.force_login(self.actor)
        self.assertEqual(guarded.post(self.url, self.action).status_code, 403)
        self.assertEqual(self.client.post(self.url, {**self.action, "intent":"verify", "page_number":-1}).status_code, 422)
        self.assertEqual(lire_brouillon(self.actor, self.site.pk)["id"], self.head["id"])
        self.grant.level = "read"
        self.grant.save()
        self.assertNotContains(self.client.get(self.url, self.selection), "Associer un article Wagtail")
        self.assertEqual(self.client.post(self.url, self.action).status_code, 403)

    def test_verification_then_confirmation_use_presented_observation(self):
        from unittest.mock import patch
        from uuid import uuid4

        proposal = {"status":"ok", "token":str(uuid4()), "page_number":42, "published_revision":"7"}
        payload = {**self.action, "page_number":42, "intent":"verify"}
        with patch("composition.editorial.verifier_article", return_value=proposal) as verify:
            response = self.client.post(self.url, payload)
        self.assertContains(response, "Révision publiée observée 7")
        self.assertContains(response, "Associer l’article")
        self.assertContains(response, proposal["token"])
        verify.assert_called_once_with(self.actor, self.site.pk, 42)
        self.assertEqual(lire_brouillon(self.actor, self.site.pk)["id"], self.head["id"])
        with patch("composition.editorial.confirmer_article", return_value=(self.head, None)) as confirm:
            response = self.client.post(self.url + "canvas/", {
                **payload, "intent":"confirm", "page_number":99, "observation":proposal["token"]})
        self.assertEqual(response.status_code, 302)
        confirm.assert_called_once_with(self.actor, self.site.pk, self.head["id"], proposal["token"],
                                        page=self.selection["page"], parent=self.selection["section"], node=None)

    def test_unavailable_and_inaccessible_keep_local_draft(self):
        from unittest.mock import patch

        for status, label in (("inaccessible", "Référence à vérifier"),
                              ("unavailable", "Vérification éditoriale indisponible")):
            with patch("composition.editorial.verifier_article", return_value={"status":status}):
                response = self.client.post(self.url, {**self.action, "page_number":42, "intent":"verify"})
            self.assertContains(response, label)
            self.assertNotContains(response, 'name="observation"')
            self.assertNotContains(response, "Associer l’article")
        self.assertEqual(lire_brouillon(self.actor, self.site.pk)["id"], self.head["id"])

    def test_article_roundtrip_comparison_conflicts_and_reader(self):
        from unittest.mock import patch
        from uuid import uuid4

        from django.utils import timezone
        from raccordement.models import SiteConnection

        now = timezone.now()
        SiteConnection.objects.create(site=self.site, instance_id=uuid4(), confirmed_profile="fixture",
            confirmed_at=now, started_at=now, finished_at=now, expires_at=now, attempt_id=uuid4(),
            diagnostic="connected", versions={"capabilities": ["editorial.published.v1"]})
        with (patch("composition.editorial._profile", return_value=object()),
              patch("composition.editorial.read_published_article", return_value="7") as remote,
              patch("composition.editor_views.editorial_admin_url", return_value="https://exemple.test/admin/") as admin):
            payload = {**self.action, "page_number":42}
            first = self.client.post(self.url, {**payload, "intent":"verify"}).context["proposal"]
            insert = self.client.post(self.url, {**payload, "intent":"confirm", "observation":first["token"]})
            self.assertEqual(insert.status_code, 302)
            current = lire_brouillon(self.actor, self.site.pk)
            selected = current["document"]["pages"][0]["sections"][0]["blocks"][-1]
            local = {**payload, "node":selected["id"], "base":current["id"]}
            canvas = self.url + "canvas/"
            count = remote.call_count
            opened = self.client.get(canvas, {**self.selection, "node":selected["id"]})
            self.assertContains(opened, "Révision Wagtail conservée dans Studio")
            self.assertContains(opened, "https://exemple.test/admin/")
            self.assertNotContains(opened, selected["props"]["content"]["ref_id"])
            self.assertEqual(remote.call_count, count)

            remote.return_value = "9"
            check = self.client.post(canvas, {**local, "intent":"verify"})
            self.assertContains(check, "Adopter la révision publiée 9")
            self.assertContains(check, "Conserver la référence")
            proposed = {**local, "intent":"confirm", "observation":check.context["proposal"]["token"]}
            self.assertEqual(self.client.post(self.url, {**self.selection, "action":"section_add",
                "base":current["id"], "display":"stack"}).status_code, 302)
            count = remote.call_count
            self.assertContains(self.client.post(canvas, proposed), "Le brouillon a changé", status_code=409)
            reread = self.client.post(canvas, {**proposed, "relire":1})
            self.assertContains(reread, "Adopter la révision publiée 9")
            self.assertEqual(remote.call_count, count)
            proposed["base"] = reread.context["base"]
            remote.return_value = "11"
            changed = self.client.post(canvas, proposed)
            self.assertContains(changed, "Adopter la révision publiée 11", status_code=409)
            self.assertEqual(lire_brouillon(self.actor, self.site.pk)["id"], proposed["base"])
            self.assertEqual(self.client.post(self.url, {**proposed,
                "observation":changed.context["proposal"]["token"]}).status_code, 302)
            self.grant.level = "read"
            self.grant.save()
            count = remote.call_count
            admin.reset_mock()
            opened = self.client.get(self.url, {**self.selection, "node":selected["id"]})
            self.assertContains(opened, "Révision publiée observée 11")
            self.assertContains(opened, "Lecture seule")
            self.assertNotContains(opened, "https://exemple.test/admin/")
            self.assertNotContains(opened, "Vérifier ou remplacer")
            self.assertEqual(remote.call_count, count)
            admin.assert_not_called()

    def test_historical_article_with_text_or_missing_content_can_be_selected(self):
        from unittest.mock import patch
        from uuid import uuid4
        from composition.catalogue import installer_version
        from composition.services import creer_brouillon

        for props in ({"content":"ancien texte"}, {}):
            archive = Site.objects.create(client=self.site.client, name="Archive")
            SiteGrant.objects.create(user=self.actor, site=archive, level="manage")
            page, section, node = (str(uuid4()) for _ in range(3))
            block = {"id":node, "definition":{"scope":"site", "key":"archive", "version":1},
                     "props":props, "children":[]}
            document = {"schema_version":1, "theme":{}, "menus":[], "pages":[{
                "id":page, "parent_id":None, "slug":"", "title":"Accueil", "sections":[{
                    "id":section, "layout":{"base":{}}, "blocks":[block]}]}]}
            creer_brouillon(self.actor, archive.pk, {"kind":"blank"}, document,
                            resolve_definition=lambda *args: {key:"text" for key in props})
            installer_version(archive, "archive", 1, "Article historique", "article")
            for suffix in ("", "canvas/"):
                url = f"/sites/{archive.pk}/atelier/{suffix}"
                selection = {"page":page, "section":section, "node":node}
                with patch("composition.editorial.lire_article") as lookup:
                    view = self.client.get(url, selection)
                    self.assertContains(view, "Référence à vérifier")
                    self.assertContains(view, "Vérifier ou remplacer la référence")
                    self.assertContains(self.client.get(url, {**selection, "action":"article_reference"}),
                                        "Vérifier la source")
                    lookup.assert_not_called()
