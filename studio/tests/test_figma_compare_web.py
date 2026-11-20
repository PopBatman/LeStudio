from unittest.mock import patch
from uuid import uuid4

from django.test import Client, TestCase
from django.urls import reverse

from composition.models import CompositionRevision, PreviewTicket
from depots import imports, services

from .test_figma_imports import ImportFixtures


class ComparisonWebTests(ImportFixtures, TestCase):
    def setUp(self):
        super().setUp()
        review = self.review()
        self.analysis = imports.confirm(*self.args, review.token)
        self.rev = self.analysis.result_revision
        self.page = self.rev.document["pages"][0]["id"]
        self.client.force_login(self.manager)
        self.url = reverse("registre:figma-compare", args=[self.site.pk, self.rev.pk, self.page])
        self.canvas = reverse("registre:site-builder", args=[self.site.pk])

    def test_private_comparison_uses_confirmed_page_without_provider(self):
        self.load.reset_mock()
        self.assertContains(self.client.get(self.canvas), self.url)
        response = self.client.get(self.url)
        self.assertEqual(response.context["frame"]["id"], "2:3")
        self.assertFalse(response.context["decision_allowed"])
        self.assertIsNone(self.client.get(self.url, {"format": "desktop"}).context["frame"])
        self.assertEqual(self.client.get(self.url, {"frame": "9:9"}).status_code, 404)
        self.load.assert_not_called()
        state = self.client.head(self.url)["X-Compare-State"]
        services.erase_submission(*self.args)
        self.assertNotEqual(self.client.head(self.url)["X-Compare-State"], state)
        self.grant.level = "read"
        self.grant.save()
        self.assertNotContains(self.client.get(self.canvas), self.url)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.assertEqual(CompositionRevision.objects.count(), 1)

    def test_receipt_preparation_scope_and_csrf(self):
        browser = Client(enforce_csrf_checks=True)
        browser.force_login(self.manager)
        self.assertEqual(browser.post(self.url, {"action": "prepare"}).status_code, 403)
        with patch("composition.preview_views.render_preview") as engine:
            engine.return_value = {"html": "<html></html>", "manifest": {"instance_id": str(uuid4())}}
            response = self.client.post(self.url, {"action": "prepare"})
            self.assertEqual(response.status_code, 302)
            ticket = PreviewTicket.objects.get()
            self.assertIn(str(ticket.pk), response.url)
            show = self.client.get(response.url)
            self.assertEqual(
                show.context["document_url"],
                reverse("registre:preview-document", args=[self.site.pk, ticket.pk]),
            )
            self.assertEqual(self.client.get(self.url, {"ticket": "invalide"}).status_code, 404)
        self.assertEqual(self.client.post(self.url, {"action": "decide"}).status_code, 422)

    def test_normal_page_imported_page_and_decision_links(self):
        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        from depots.models import ComparisonDecision, FrameReference

        self.analysis.observation["frames"][0].update(width=390, height=800)
        self.analysis.save(update_fields=["observation"])
        buffer = BytesIO()
        Image.new("RGB", (195, 400), "white").save(buffer, format="PNG")
        upload = SimpleUploadedFile("frame.png", buffer.getvalue(), content_type="image/png")
        attachment = {
            "action": "attach",
            "confirmed": "1",
            "image": upload,
            "version": "v1",
            "format": "mobile",
        }
        self.assertEqual(self.client.post(self.url, attachment).status_code, 302)
        reference = FrameReference.objects.get()
        response = self.client.get(self.url)
        self.assertEqual(self.client.get(response.context["reference_url"]).status_code, 200)
        occurrence = self.analysis.mapping["2:4"]
        target_row = next(r for r in response.context["frame"]["rows"] if r["occurrence"] == occurrence)
        editor = self.client.get(target_row["edit_url"])
        self.assertTrue(editor.context["builder_edit"]["open_editor"])
        self.assertEqual(editor.context["builder_edit"]["selection"], occurrence)

        with patch("composition.preview_views.render_preview") as engine:
            engine.return_value = {
                "html": "<html></html>",
                "manifest": {"instance_id": str(uuid4()), "block_ids": [occurrence]},
            }
            location = self.client.post(self.url, {"action": "prepare"}).url
            review = self.client.get(location)
            ticket = review.context["ticket"]
            self.assertTrue(review.context["decision_allowed"])
            payload = {
                "action": "decide",
                "confirmed": "1",
                "ticket": str(ticket),
                "kind": "accepted",
                "note": "Écart examiné",
                "key": str(uuid4()),
                "reference": str(reference.pk),
                "width": "390",
            }
            self.assertEqual(self.client.post(location, payload).status_code, 302)
            self.assertEqual(self.client.post(location, payload).status_code, 302)
            self.assertEqual(ComparisonDecision.objects.count(), 1)
            self.assertEqual(self.client.get(location).context["current_state"], "Écart accepté")
            payload["key"] = str(uuid4())
            conflict = self.client.post(location, payload)
            self.assertEqual(conflict.status_code, 409)
            self.assertEqual(conflict.context["draft_note"], payload["note"])
        self.assertEqual(CompositionRevision.objects.count(), 1)
