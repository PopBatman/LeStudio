from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import TestCase, Client as Browser

from composition.models import CompositionRevision
from depots.models import Invitation, Submission
from registre.models import Client, Site, SiteGrant
from workspace.access import OPERATOR_GROUP


class ImportWebTests(TestCase):
    def setUp(self):
        self.actor = User.objects.create_user("gestion")
        self.actor.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        client = Client.objects.create(display_name="Papeterie", client_type="COMPANY")
        self.site = Site.objects.create(name="Atelier", client=client)
        self.grant = SiteGrant.objects.create(user=self.actor, site=self.site, level="manage")
        invitation = Invitation.objects.create(site=self.site, author=self.actor,
                                               expires_at=self.actor.date_joined)
        self.row = Submission.objects.create(invitation=invitation, version=1, request_id=uuid4(),
                                             figma_url="https://www.figma.com/design/Proof1234")
        self.client.force_login(self.actor)
        self.detail = f"/sites/{self.site.pk}/depots/soumissions/{self.row.pk}/"
        self.url = self.detail + "import/"

    def test_entry_and_missing_profile(self):
        self.assertContains(self.client.get(self.detail), self.url)
        self.assertContains(self.client.get(self.url), "Analyser la maquette")
        response = self.client.post(self.url, {"action": "start"})
        self.assertContains(response, 'role="alert"', status_code=422)
        self.assertEqual(CompositionRevision.objects.count(), 0)

    def test_reader_other_site_and_csrf(self):
        self.grant.level = "read"
        self.grant.save()
        self.assertNotContains(self.client.get(self.detail), self.url)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.assertEqual(self.client.post(self.url, {"action": "start"}).status_code, 403)
        self.grant.delete()
        self.assertEqual(self.client.get(self.url).status_code, 404)
        csrf_client = Browser(enforce_csrf_checks=True)
        csrf_client.force_login(self.actor)
        self.assertEqual(csrf_client.post(self.url, {"action": "start"}).status_code, 403)

    def test_review_form_displays_source_and_preserves_bad_input(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        definition = {"id": str(uuid4()), "scope": "global", "key": "heading",
                      "version": 1, "label": "Titre", "renderer": "heading"}
        proposal = {"id": "2:3", "frame_id": "2:1", "name": "Titre des Saules", "type": "TEXT",
                    "text": "Les Saules", "candidates": [definition], "suggested": definition["id"],
                    "props": {"text": "Les Saules", "level": 2}, "tokens": {"ink": "#23344B"}}
        a = SimpleNamespace(state="review", decisions={}, proposals=[proposal], destinations=[],
                            observation={"frames": [{"id":"2:1","name":"Page","nodes":[]}]}, token=uuid4())
        with patch("depots.import_views.imports.current", return_value=a):
            url = self.url + "?screen=node&node=2%3A3"
            self.assertContains(self.client.get(url), "Couleur du texte")
            result = self.client.post(url, {"screen": "node", "action": "decision", "verdict": "accept",
                "definition": definition["id"], "token": str(a.token), "text": "Une correction",
                "level": "2", "pick_ink": "edit", "ink": "invalide"})
            self.assertContains(result, "Une correction", status_code=422)
            self.assertContains(result, 'role="alert"', status_code=422)
