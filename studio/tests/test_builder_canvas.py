from datetime import timedelta
from base64 import b64encode
from hashlib import sha256
from html.parser import HTMLParser
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import Client as Browser, TestCase
from django.urls import reverse
from django.utils import timezone

from composition.models import BuilderSave, CompositionRevision, PreviewTicket
from composition.preview import PreviewError
from composition.services import creer_brouillon, modifier_navigation
from registre.models import Client, Site, SiteGrant
from workspace.access import OPERATOR_GROUP

from .test_composition_services import sample_document


class EmbeddedModule(HTMLParser):
    def __init__(self):
        super().__init__()
        self.attrs = {}
        self.script = ""
        self.reading = False

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.attrs = dict(attrs)
            self.reading = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.reading = False

    def handle_data(self, text):
        if self.reading:
            self.script += text


class BuilderCanvasTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("lectrice-canvas")
        self.user.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        owner = Client.objects.create(display_name="Site de recette", client_type="COMPANY")
        self.site = Site.objects.create(client=owner, name="Papeterie")
        self.grant = SiteGrant.objects.create(user=self.user, site=self.site, level="manage")
        self.other = Site.objects.create(client=owner, name="Autre site")
        self.doc = sample_document()
        self.rev = creer_brouillon(self.user, self.site.pk, {"kind": "blank"}, self.doc)
        self.page = self.rev["document"]["pages"][0]
        self.params = {"revision": self.rev["id"], "page": self.page["id"]}
        self.grant.level = "read"
        self.grant.save()
        self.client.force_login(self.user)
        self.home = reverse("registre:site-builder", args=[self.site.pk])
        self.blocks = self.page["sections"][0]["blocks"]
        content = "".join(f'<div data-studio-block-id="{b["id"]}">Titre</div>' for b in self.blocks)
        self.source = "<!doctype html>\n<html lang=\"fr\"><head></head><body><main>" + content + "</main></body></html>\n"
        self.engine = patch("composition.preview_views.render_preview").start()
        self.engine.return_value = {
            "html": self.source,
            "manifest": {"site_id": str(self.site.pk), "instance_id": str(uuid4()),
                         "revision_id": self.rev["id"], "page_id": self.page["id"],
                         "block_ids": [b["id"] for b in self.blocks]},
        }
        self.addCleanup(patch.stopall)

    def ticket(self):
        response = self.client.post(self.home, self.params)
        self.assertEqual(response.status_code, 302)
        ticket = PreviewTicket.objects.get()
        self.assertEqual(response.url, reverse("registre:builder-view", args=[self.site.pk, ticket.pk]))
        return ticket, response.url

    def test_renders_verified_source_and_pins_static_module_for_read_only_site(self):
        ticket, address = self.ticket()
        ctx = self.client.get(address).context
        self.assertTrue(ctx['available'])
        self.assertEqual([layer['id'] for layer in ctx['layers']], [b["id"] for b in self.blocks])
        frame = self.client.get(address + "document/")
        parser = EmbeddedModule()
        parser.feed(frame.content.decode())
        self.assertTrue(parser.script)
        digest = b64encode(sha256(parser.script.encode()).digest()).decode()
        self.assertIn(f"script-src 'sha256-{digest}'", frame["Content-Security-Policy"])
        self.assertNotIn("allow-same-origin", frame["Content-Security-Policy"])
        self.assertIn("no-store", frame["Cache-Control"])
        self.assertGreaterEqual(int(frame["Refresh"]), 1)
        self.assertLessEqual(int(frame["Refresh"]), 600)
        self.assertEqual(parser.attrs["data-fingerprint"], ticket.fingerprint)
        self.assertEqual(parser.attrs["data-page"], self.page['id'])
        self.assertEqual(frame['X-Studio-Head-Has-Page'], '1')
        ref = self.client.get(reverse("registre:preview-document", args=[self.site.pk, ticket.pk]))
        self.assertEqual(ref.content.decode(), self.source)
        self.assertNotIn("allow-scripts", ref["Content-Security-Policy"])
        self.assertEqual(CompositionRevision.objects.count(), 1)

    def test_save_confirmation_survives_preview_redirect_for_the_recorded_revision(self):
        params = {**self.params, "saved": "1"}
        self.assertNotContains(self.client.post(self.home, params, follow=True), "Le brouillon est enregistré")
        BuilderSave.objects.create(site=self.site, operator=self.user, key=uuid4(), fingerprint="a" * 64,
                                   revision_id=self.rev["id"], mapping={})
        response = self.client.post(self.home, params, follow=True)
        self.assertContains(response, "Le brouillon est enregistré en R1.")
        self.assertNotContains(response, "L’aperçu pourra être préparé de nouveau.")
        self.assertNotContains(self.client.post(self.home, self.params, follow=True), "Le brouillon est enregistré")

    def test_receipt_is_bound_to_session_and_site_and_fails_closed(self):
        ticket, address = self.ticket()
        other = Browser()
        other.force_login(self.user)
        self.assertEqual(other.get(address + "document/").status_code, 404)
        SiteGrant.objects.create(user=self.user, site=self.other, level="read")
        self.assertEqual(self.client.get(reverse("registre:builder-document", args=[self.other.pk, ticket.pk])).status_code, 404)
        self.engine.return_value["html"] += " "
        changed = self.client.get(address + "document/")
        self.assertEqual(changed.status_code, 409)
        self.assertNotIn(b"<script", changed.content)
        self.assertEqual(self.client.get(address).context["layers"][0]["id"], self.blocks[0]["id"])
        PreviewTicket.objects.filter(pk=ticket.pk).update(expires_at=timezone.now() - timedelta(seconds=1))
        self.assertEqual(self.client.head(address + "document/").status_code, 410)
        self.grant.delete()
        self.assertEqual(self.client.get(address).status_code, 404)
        self.assertEqual(self.client.get(self.home, {**self.params, "mode": "structure"}).status_code, 404)

    def test_unavailable_falls_back_to_authorized_structure_and_historical_receipt(self):
        self.engine.side_effect = PreviewError("unavailable")
        result = self.client.post(self.home, self.params)
        self.assertEqual(result.status_code, 409)
        self.assertEqual(len(result.context["layers"]), 2)
        self.assertFalse(PreviewTicket.objects.exists())
        self.engine.reset_mock()
        fallback = self.client.get(self.home, {**self.params, "mode": "structure"})
        self.assertEqual(fallback.status_code, 200)
        self.assertTrue(fallback.context['structure_only'])
        self.engine.assert_not_called()
        self.engine.side_effect = None
        _, address = self.ticket()
        self.grant.level = "manage"
        self.grant.save()
        saved = modifier_navigation(self.user, self.site.pk, self.rev["id"], {
            "action": "page_edit", "id": self.page["id"], "title": "Nouveau titre", "slug": ""})
        ctx = self.client.get(address).context
        self.assertEqual(ctx["revision"]["id"], self.rev["id"])
        self.assertEqual(ctx["head"]["id"], saved["id"])
        self.assertEqual(self.client.head(address + "document/")["X-Studio-Head"], "2")
        self.assertEqual(CompositionRevision.objects.count(), 2)

    def test_failed_health_check_hides_structure_if_access_was_lost_in_flight(self):
        _, address = self.ticket()

        def revoke_during_render(*args):
            self.grant.delete()
            raise PreviewError("unavailable")

        self.engine.side_effect = revoke_during_render
        self.assertEqual(self.client.head(address + "document/").status_code, 404)

    def test_unknown_document_shape_does_not_enable_selection(self):
        self.engine.return_value['html'] = '<p>Page sans enveloppe reconnue</p>'
        _, address = self.ticket()
        self.assertFalse(self.client.get(address).context['available'])
        response = self.client.get(address + "document/")
        self.assertEqual(response.status_code, 409)
        self.assertNotIn(b"<script", response.content)
