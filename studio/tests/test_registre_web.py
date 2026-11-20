from django.test import TestCase

from django.contrib.auth.models import Group, User
from workspace.access import OPERATOR_GROUP


class RegistryPageTests(TestCase):
    def test_anonymous_and_operator_entry(self):
        self.assertEqual(self.client.get("/clients/").status_code, 302)
        operator = User.objects.create_user("demo")
        operator.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        self.client.force_login(operator)
        self.assertContains(self.client.get("/clients/"), "Aucun client")
        self.assertContains(self.client.get("/sites/"), "Aucun site")
        self.assertEqual(self.client.get("/clients/nouveau/").status_code, 403)

    def test_invalid_filter_is_rejected(self):
        operator = User.objects.create_user("lecteur")
        operator.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        self.client.force_login(operator)
        for url, data in (("/sites/", {"q": "x\0y"}), ("/clients/", {"type": "inconnu"})):
            self.assertContains(self.client.post(url, data), "Recherche invalide", status_code=400)


class RegistryWorkflowTests(TestCase):
    def setUp(self):
        from registre.models import Client, Site, SiteGrant

        self.operator = User.objects.create_user("atelier")
        self.operator.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        self.client.force_login(self.operator)
        self.owner = Client.objects.create(display_name="Client confidentiel", client_type="COMPANY")
        self.site = Site.objects.create(name="Journal", client=self.owner)
        self.sibling = Site.objects.create(name="Boutique privée", client=self.owner)
        SiteGrant.objects.create(user=self.operator, site=self.site, level="manage")
        self.url = f"/sites/{self.site.pk}/"

    def test_site_only_access_survives_edit_without_disclosing_its_owner(self):
        for route in ("/sites/", self.url, self.url + "modifier/"):
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, self.owner.display_name)
            self.assertNotContains(response, self.owner.pk)
            self.assertNotContains(response, self.sibling.name)
        self.assertEqual(self.client.get(f"/sites/{self.sibling.pk}/").status_code, 404)
        self.assertEqual(self.client.get(f"/clients/{self.owner.pk}/").status_code, 404)
        payload = {"name": "Journal du soir", "version": self.site.updated_at.isoformat()}
        self.assertRedirects(self.client.post(self.url + "modifier/", payload),
                             self.url + "?resultat=enregistre")
        self.assertEqual(self.client.post(self.url + "modifier/", payload).status_code, 409)

    def test_contact_validation_and_archive_preserve_site_access(self):
        from registre.models import ClientGrant

        ClientGrant.objects.create(client=self.owner, user=self.operator, level="manage")
        base = f"/clients/{self.owner.pk}/"
        fields = {"display_name": "Interlocuteur fictif", "role": "Direction"}
        response = self.client.post(base + "contacts/nouveau/", fields)
        self.assertContains(response, "Renseignez au moins une coordonnée")
        self.assertFalse(self.owner.contacts.exists())
        response = self.client.post(base + "contacts/nouveau/", {**fields, "phone": "01 23 45 67 89"})
        self.assertRedirects(response, base + "?resultat=enregistre")
        self.assertEqual(self.owner.contacts.get().phone, "0123456789")
        self.assertRedirects(self.client.post(base + "archiver/", {"version": self.owner.updated_at.isoformat()}),
                             base + "?resultat=archive")
        self.assertContains(self.client.get("/clients/?etat=archives"), self.owner.display_name)
        self.assertNotContains(self.client.get("/clients/"), self.owner.display_name)
        self.assertEqual(self.client.get(base + "contacts/nouveau/").status_code, 403)
        self.assertEqual(self.client.get(self.url + "modifier/").status_code, 200)
