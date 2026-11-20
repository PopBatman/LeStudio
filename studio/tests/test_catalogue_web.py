from django.contrib.auth.models import Group, User
from django.test import Client as WebClient

from composition.services import creer_brouillon, lire_brouillon
from registre.models import Client, Site, SiteGrant
from tests.catalogue_fixture import CatalogueTestCase
from workspace.access import OPERATOR_GROUP


class CatalogueWebTests(CatalogueTestCase):
    def setUp(self):
        self.user = User.objects.create_user("gestion")
        self.user.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        owner = Client.objects.create(display_name="Maison témoin", client_type="COMPANY")
        self.site = Site.objects.create(client=owner, name="Maison des dunes")
        self.grant = SiteGrant.objects.create(user=self.user, site=self.site, level="manage")
        self.client.force_login(self.user)
        self.url = f"/sites/{self.site.pk}/"
        self.library = self.url + "bibliotheque/"
        self.appearance = self.url + "apparence/"

    def test_empty_site_permissions_and_direct_access(self):
        self.assertContains(self.client.get(self.url), self.library)
        self.assertContains(self.client.get(self.library), "Bouton")
        self.assertNotContains(self.client.get(self.library), 'name="block"')
        self.assertContains(self.client.get(self.appearance), self.url + "pages/")
        csrf = WebClient(enforce_csrf_checks=True)
        csrf.force_login(self.user)
        self.assertEqual(csrf.post(self.appearance, {"action": "theme"}).status_code, 403)
        self.grant.level = "read"
        self.grant.save()
        self.assertNotContains(self.client.get(self.appearance), "Enregistrer le thème")
        self.assertEqual(self.client.post(self.appearance, {"action": "theme"}).status_code, 403)
        self.grant.delete()
        self.assertEqual(self.client.get(self.library).status_code, 404)

    def test_appearance_saved_and_stale_submission_keeps_values(self):
        head = creer_brouillon(self.user, self.site.pk, {"kind": "blank"})
        values = {"action": "theme", "base": head["id"], "accent": "#114488", "gap": "18"}
        self.assertEqual(self.client.post(self.appearance, values).status_code, 302)
        current = lire_brouillon(self.user, self.site.pk)
        self.assertEqual(current["document"]["theme"], {"accent": "#114488", "gap": 18})
        self.assertContains(self.client.get(self.appearance), "#114488")
        values["accent"] = "#882211"
        conflict = self.client.post(self.appearance, values)
        self.assertContains(conflict, "#882211", status_code=409)
        self.assertEqual(lire_brouillon(self.user, self.site.pk)["id"], current["id"])

    def test_occurrence_candidate_and_public_library_without_draft_mutation(self):
        from uuid import uuid4
        from composition.catalogue import installer_version
        from composition.models import ComponentVersion

        key = lambda: str(uuid4())
        block = {"id": key(), "definition": {"scope": "global", "key": "text", "version": 1},
                 "props": {"text": "Texte de départ"}, "children": []}
        doc = {"schema_version": 1, "theme": {}, "menus": [], "pages": [{
            "id": key(), "parent_id": None, "slug": "", "title": "Accueil",
            "sections": [{"id": key(), "layout": {"base": {"display": "stack"}}, "blocks": [block]}]}]}
        head = creer_brouillon(self.user, self.site.pk, {"kind": "blank"}, doc)
        candidate = installer_version(self.site, "signature", 1, "Signature locale", "signature")
        params = {"action": "block", "block": block["id"], "definition": str(candidate.pk)}
        self.assertContains(self.client.get(self.library, params), "Version proposée")
        self.assertContains(self.client.get(self.library, {"block": block["id"]}),
                            f'name="block" value="{block["id"]}"')
        self.assertContains(self.client.get(self.library, params), f'name="block" value="{block["id"]}"')
        self.assertEqual(self.client.post(self.library, {
            **params, "base": head["id"], "prop_text": "Nos ateliers", "accent": "#663311"
        }).status_code, 302)
        current = lire_brouillon(self.user, self.site.pk)
        saved = current["document"]["pages"][0]["sections"][0]["blocks"][0]
        self.assertEqual(saved["props"], {"text": "Nos ateliers"})
        self.assertEqual(saved["definition"]["key"], "signature")
        self.assertEqual(saved["appearance"]["tokens"]["accent"], "#663311")
        self.assertContains(self.client.get(self.library, {"block": block["id"]}), "Signature locale")
        button = ComponentVersion.objects.get(site=None, key="button", version=1)
        params = {"action": "preference", "definition": str(button.pk)}
        self.assertContains(self.client.get(self.library, params), "Préférence du site")
        self.assertEqual(self.client.post(self.library, {**params, "base": current["id"], "variant": "secondary"}).status_code, 302)
        current = lire_brouillon(self.user, self.site.pk)
        self.assertEqual(current["document"]["theme"]["components"][0]["variant"], "secondary")

    def test_promotion_requires_independent_review_and_proof(self):
        from composition.catalogue import REVIEW_GROUP, installer_version
        from composition.models import Promotion

        local = installer_version(self.site, "signature", 1, "Signature locale", "signature")
        params = {"action": "propose", "definition": str(local.pk)}
        self.assertContains(self.client.get(self.library, params), "Justificatif".lower())
        self.assertEqual(self.client.post(self.library, {**params, "key": "signature-partagee",
                         "label": "Signature partagée", "rights": "Autorisation DEMO", "reason": "Rendu réutilisable"}).status_code, 302)
        proposal = Promotion.objects.get()
        review = {"action": "review", "proposal": str(proposal.pk), "fingerprint": proposal.fingerprint,
                  "decision": "approve", "note": "Revue de démonstration"}
        self.assertEqual(self.client.post(self.library, review).status_code, 403)
        reviewer = User.objects.create_user("relectrice")
        reviewer.groups.add(Group.objects.get(name=OPERATOR_GROUP), Group.objects.get_or_create(name=REVIEW_GROUP)[0])
        SiteGrant.objects.create(user=reviewer, site=self.site, level="manage")
        self.client.force_login(reviewer)
        self.assertContains(self.client.get(self.library, {"action": "review", "proposal": proposal.pk}), "Autorisation DEMO")
        self.assertEqual(self.client.post(self.library, review).status_code, 422)
        self.assertEqual(self.client.post(self.library, {**review, "rights_checked": "on", "technical_checked": "on"}).status_code, 302)
        self.assertContains(self.client.get(self.library, {"scope": "global"}), "Signature partagée")

    def test_unavailable_preference_can_be_removed_without_installing_its_definition(self):
        from composition.models import CompositionRevision

        head = creer_brouillon(self.user, self.site.pk, {"kind": "blank"})
        doc = head["document"]
        doc["schema_version"] = 3
        missing = {"scope": "site", "key": "ancienne-version", "version": 3}
        doc["theme"] = {"components": [{"definition": missing, "variant": "default"}]}
        CompositionRevision.objects.filter(pk=head["id"]).update(document=doc)
        self.assertContains(self.client.get(self.library), "Retirer ce réglage de version")
        remove = {"action": "clear_preference", **{"pref_" + k: str(v) for k, v in missing.items()}}
        confirmation = self.client.get(self.library, remove)
        self.assertContains(confirmation, 'name="pref_key" value="ancienne-version"')
        response = self.client.post(self.library, {**remove, "base": head["id"], "confirmed": "on"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(lire_brouillon(self.user, self.site.pk)["document"]["theme"], {})
