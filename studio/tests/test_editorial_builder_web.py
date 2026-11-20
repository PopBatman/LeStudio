from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import Client as HttpClient
from django.utils import timezone

from composition.editor import creer_atelier
from composition.services import lire_brouillon
from raccordement.models import SiteConnection
from registre.models import Client, Site, SiteGrant
from tests.catalogue_fixture import CatalogueTestCase
from workspace.access import OPERATOR_GROUP


class BuilderArticleTests(CatalogueTestCase):
    def setUp(self):
        self.actor = User.objects.create_user("gestion")
        self.actor.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        owner = Client.objects.create(display_name="Démo", client_type="COMPANY")
        self.site = Site.objects.create(client=owner, name="Éditorial")
        self.grant = SiteGrant.objects.create(user=self.actor, site=self.site, level="manage")
        self.client.force_login(self.actor)
        self.url = f"/sites/{self.site.pk}/atelier/articles/"
        self.head = creer_atelier(self.actor, self.site.pk, "template")
        page = self.head["document"]["pages"][0]
        self.target = {"page": page["id"], "selection": page["sections"][0]["id"]}
        self.data = {**self.target, "base": self.head["id"], "page_number": 42}

    def test_compare_confirm_keep_replace_and_read(self):
        now = timezone.now()
        SiteConnection.objects.create(site=self.site, instance_id=uuid4(), confirmed_profile="fixture",
            confirmed_at=now, started_at=now, finished_at=now, expires_at=now, attempt_id=uuid4(),
            diagnostic="connected", versions={"capabilities": ["editorial.published.v1"]})
        with (patch("composition.editorial._profile", return_value=object()),
              patch("composition.editorial.read_published_article", return_value="7") as remote):
            self.assertContains(self.client.get(self.url, self.target), "Vérifier la source")
            first = self.client.post(self.url, {**self.data, "intent":"verify"})
            self.assertContains(first, "Associer l’article")
            confirm = {**self.data, "intent":"confirm", "observation":first.context["proposal"]["token"]}
            linked = self.client.post(self.url, confirm)
            node = lire_brouillon(self.actor, self.site.pk)["document"]["pages"][0]["sections"][0]["blocks"][-1]
            self.assertIn("selection=" + node["id"], linked.url)
            self.assertContains(self.client.post(self.url, confirm), "Le brouillon a changé", status_code=409)
            target = {**self.target, "selection":node["id"]}
            data = {**self.data, **target, "base":lire_brouillon(self.actor, self.site.pk)["id"]}
            remote.return_value = "8"
            observed = self.client.post(self.url, {**data, "intent":"verify"})
            self.assertContains(observed, "Adopter la révision publiée 8")
            self.assertContains(observed, "Conserver la référence")
            count = remote.call_count
            self.assertContains(self.client.get(self.url, target), "Révision publiée observée 8")
            self.assertEqual(remote.call_count, count)
            self.assertEqual(lire_brouillon(self.actor, self.site.pk)["id"], data["base"])
            adopted = self.client.post(self.url, {**data, "intent": "confirm",
                                        "observation": observed.context["proposal"]["token"]})
            self.assertIn("selection=" + node["id"], adopted.url)
            pinned = self.client.get(self.url, target).context["article"]
            self.assertEqual((pinned["page_number"], pinned["expected_revision"]), (42, "8"))
            data["base"] = lire_brouillon(self.actor, self.site.pk)["id"]
            other = self.client.post(self.url, {**data, "intent":"verify", "page_number":43})
            self.assertContains(other, "Remplacer la référence")
            remote.return_value = "9"
            changed = self.client.post(self.url, {**data, "intent": "confirm",
                                                   "observation": other.context["proposal"]["token"]})
            self.assertContains(changed, "La source a changé", status_code=409)
            self.assertEqual(lire_brouillon(self.actor, self.site.pk)["id"], data["base"])
            saved = self.client.post(self.url, {**data, "intent": "confirm",
                                                "observation": changed.context["proposal"]["token"]})
            self.assertIn("selection=" + node["id"], saved.url)
            latest = lire_brouillon(self.actor, self.site.pk)
            self.assertContains(self.client.get(self.url, target), "Révision publiée observée 9")
            historical = self.client.get(self.url, {**target, "revision": data["base"]})
            self.assertContains(historical, "Révision historique")
            self.assertNotContains(historical, "Vérifier la source")
            data["base"] = latest["id"]
            self.grant.level = "read"
            self.grant.save()
            read = self.client.get(self.url, target)
            self.assertContains(read, "Lecture seule")
            self.assertNotContains(read, "Vérifier la source")
            self.assertEqual(self.client.post(self.url, {**data, "intent":"confirm",
                             "observation":other.context["proposal"]["token"]}).status_code, 403)
            self.assertEqual(lire_brouillon(self.actor, self.site.pk)["id"], data["base"])

    def test_invalid_target_and_unavailable_source(self):
        guarded = HttpClient(enforce_csrf_checks=True)
        guarded.force_login(self.actor)
        self.assertEqual(guarded.post(self.url, self.data).status_code, 403)
        other = Site.objects.create(client=self.site.client, name="Autre")
        other_url = f"/sites/{other.pk}/atelier/articles/"
        self.assertEqual(self.client.get(other_url, self.target).status_code, 404)
        self.assertEqual(self.client.post(other_url, self.data).status_code, 404)
        self.assertEqual(self.client.get(self.url, {**self.target, "selection":uuid4()}).status_code, 404)
        with patch("composition.editorial.verifier_article", return_value={"status":"unavailable"}):
            result = self.client.post(self.url, {**self.data, "intent":"verify"})
        self.assertContains(result, "Vérification éditoriale indisponible")
        self.assertNotContains(result, 'name="observation"')
        self.assertEqual(lire_brouillon(self.actor, self.site.pk)["id"], self.head["id"])
