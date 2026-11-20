from copy import deepcopy
from datetime import timedelta
from unittest.mock import patch
from uuid import uuid4

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from composition.editor import creer_atelier
from composition.models import CompositionRevision
from depots import imports, provenance, services
from depots.models import Submission
from .test_figma_imports import ImportFixtures


class FigmaProvenanceTests(ImportFixtures, TestCase):
    def confirmed(self, append=False):
        row = self.review(append=append)
        return imports.confirm(*self.args, row.token)

    def context(self, revision, page):
        return provenance.for_page(self.manager, self.site.pk, revision.pk, page)

    def test_confirmed_frame_section_and_unknown_task_with_no_network(self):
        result = self.confirmed()
        rev = result.result_revision
        page = rev.document["pages"][0]
        self.load.reset_mock()
        self.inventory.reset_mock()
        source = self.context(rev, page["id"])
        self.assertEqual(source["analysis_id"], str(result.pk))
        self.assertEqual(source["version"], "v1")
        self.assertEqual(source["submission_number"], 1)
        self.assertEqual(source["author"], self.manager.get_username())
        self.assertEqual(source["missing_formats"], ["desktop", "tablet"])
        frame, = source["frames"]
        self.assertEqual(frame["section_id"], page["sections"][0]["id"])
        self.assertEqual(frame["format"], "mobile")
        root, body, excluded = frame["rows"]
        self.assertEqual(root["occurrence"], result.mapping["2:3@container"])
        self.assertEqual(body["definition"]["version"], 1)
        self.assertFalse(excluded["selectable"])
        self.assertEqual(excluded["decision"], "exclude")
        self.assertEqual(excluded["task"]["status"], "À instruire")
        self.assertEqual(excluded["task"], self.context(rev, page["id"])["frames"][0]["rows"][2]["task"])
        self.load.assert_not_called()
        self.inventory.assert_not_called()

    def test_replay_and_return_link_exactly_to_appended_pages(self):
        create = creer_atelier(self.manager, self.site.pk, "template")
        result = self.confirmed(append=True)
        rev = result.result_revision
        page = rev.document["pages"][-1]
        old = create["document"]["pages"][0]["id"]
        self.assertIsNone(self.context(rev, old))
        self.assertFalse(provenance.is_imported_page(self.site.pk, rev.pk, old))
        self.assertTrue(provenance.is_imported_page(self.site.pk, rev.pk, page["id"]))
        self.client.force_login(self.manager)
        url = reverse("registre:depot-import", args=[self.site.pk,self.sub.pk])
        self.load.reset_mock()
        for response in (self.client.get(url), self.client.post(url, {
            "action": "confirm", "screen": "summary", "token": result.token})):
            self.assertContains(response, f'page={page["id"]}')
            self.assertNotContains(response, f'page={old}')
        self.load.assert_not_called()

    def test_renamed_page_superseded_node_and_local_copy(self):
        result = self.confirmed()
        rev = result.result_revision
        doc = deepcopy(rev.document)
        page = doc["pages"][0]
        page["title"] = "Titre local"
        child = page["sections"][0]["blocks"][0]["children"][0]
        child["id"] = str(uuid4())
        new = CompositionRevision.objects.create(site=self.site,parent=rev,number=2,author=self.manager,document=doc)
        source = self.context(new, page["id"])
        self.assertEqual(source["import_number"], 1)
        self.assertFalse(source["frames"][0]["rows"][1]["selectable"])
        self.assertEqual([item["id"] for item in source["local_blocks"]], [child["id"]])

    def test_erased_or_expired_receipt_keeps_only_local_evidence(self):
        result = self.confirmed()
        rev = result.result_revision
        page = rev.document["pages"][0]["id"]
        Submission.objects.filter(pk=self.sub.pk).update(created_at=timezone.now()-timedelta(days=91))
        for purged in [False, True]:
            if purged:
                services.purge()
            context = self.context(rev,page)
            self.assertFalse(context["detail_available"])
            self.assertFalse(context["version"])
            self.assertFalse(context["frames"])
            self.assertEqual(context["import_number"],rev.number)

    def test_two_imports_with_same_frame_and_label_stay_on_their_page(self):
        first = self.confirmed()
        self.sub = services.submit(self.cap, uuid4(), self.url)
        self.args = self.manager, self.site.pk, self.sub.pk
        second = self.confirmed(append=True)
        rev = second.result_revision
        old, new = rev.document["pages"]
        old_source, new_source = self.context(rev, old["id"]), self.context(rev, new["id"])
        self.assertEqual((old_source["analysis_id"], new_source["analysis_id"]), (str(first.pk), str(second.pk)))
        self.assertEqual((old_source["submission_number"], new_source["submission_number"]), (1, 2))
        self.assertNotEqual(old_source["frames"][0]["rows"][-1]["task"]["id"],
                            new_source["frames"][0]["rows"][-1]["task"]["id"])

    def test_grouped_frames_keep_format_specific_projected_values(self):
        self.inventory.return_value["frames"] = [
            {"id": "1:1", "name": "Grand", "page": "Accueil"},
            {"id": "2:1", "name": "Petit", "page": "Accueil"},
        ]
        inv = imports.start(*self.args)
        frames = [
            {"id": "1:1", "name": "Grand", "width":1200, "height": 600,
             "gap": 48, "tokens": {"gap":48}, "nodes":[]},
            {"id": "2:1", "name": "Petit", "width":390, "height": 750,
             "gap": 16, "tokens": {"gap":16}, "nodes":[]},
        ]
        with patch("depots.figma.inspect_frames", return_value={"version":"v1", "frames":frames}):
            row = imports.select_frames(*self.args, inv.token, [f["id"] for f in frames])
        choices = {f["id"]: {"action":"accept"} for f in frames}
        choices["1:1"]["tokens"] = {"gap":32}
        destinations = [
            dict(group="Accueil", format=fmt, base=is_base, home=is_base, frame_id=f["id"], title="Accueil", slug="")
            for f, fmt, is_base in zip(frames, ["desktop","mobile"], [True,False])
        ]
        row = imports.save_review(*self.args, row.token, choices, destinations)
        result = imports.confirm(*self.args, row.token)
        source = self.context(result.result_revision, result.mapping["1:1"])
        self.assertEqual(source["missing_formats"], ["tablet"])
        desk, mobile = source["frames"]
        self.assertEqual((desk["width"], mobile["width"]), (1200,390))
        self.assertEqual(mobile["section_id"], desk["section_id"])
        self.assertEqual(mobile["rows"][0]["occurrence"], desk["rows"][0]["occurrence"])
        self.assertEqual(desk["rows"][0]["token_rows"], [{"name":"gap","observed":48,"value":32}])
        self.assertEqual(mobile["rows"][0]["token_rows"], [{"name":"gap","observed":16,"value":16}])

    def test_cross_site_and_readonly(self):
        result = self.confirmed()
        rev = result.result_revision
        page = rev.document["pages"][0]["id"]
        with self.assertRaises(Http404):
            provenance.for_page(self.manager, self.other.pk, rev.pk, page)
        self.grant.level = "read"
        self.grant.save()
        with self.assertRaises(PermissionDenied):
            self.context(rev,page)
