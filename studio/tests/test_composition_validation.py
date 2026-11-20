import copy
import json
from pathlib import Path
from unittest.mock import Mock, patch
import unittest
from uuid import uuid4

from django.core.exceptions import ValidationError

from composition.validation import check_document, remap_occurrence_ids


FIXTURE = Path(__file__).resolve().parents[1] / "work/items/FEAT-003-01/evidence/composition-v1.json"


class CompositionValidationTests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads(FIXTURE.read_text())
        self.site = uuid4()
        self.root, self.page = self.doc["pages"]
        self.section = self.root["sections"][0]
        self.heading, self.text = self.section["blocks"]

    def check(self, doc=None, **kwargs):
        return check_document(self.doc if doc is None else doc, self.site, **kwargs)

    def test_fixture_round_trip_and_external_ids(self):
        self.assertEqual(self.check(), self.doc)
        self.assertEqual(self.check(FIXTURE.read_bytes()), self.doc)
        copied = remap_occurrence_ids(self.check())
        self.assertEqual(self.check(copied), copied)
        parent, child = copied["pages"]
        self.assertEqual(child["parent_id"], parent["id"])
        self.assertNotEqual(parent["id"], self.root["id"])
        section = parent["sections"][0]
        self.assertNotEqual(section["id"], self.section["id"])
        for old, new in zip(self.section["blocks"], section["blocks"]):
            self.assertNotEqual(old["id"], new["id"])
            self.assertEqual(old["definition"], new["definition"])
        child["title"] = "Nouveau"
        self.assertNotEqual(child["title"], self.page["title"])

    def test_raw_syntax_and_encoding_errors(self):
        for raw in (b"\xff", '{"k":1,"k":2}', '{"n":NaN}', "[", "[]"):
            with self.subTest(raw=raw), self.assertRaises(ValidationError):
                self.check(raw)

    def test_keys_exact_types_and_version(self):
        for mapping, key, value in [
            (self.heading["props"], "level", True), (self.heading["props"], "text", "\x00"),
            (self.root, "title", "x"*121), (self.root, "id", self.root["id"].upper()),
            (self.text, "id", self.root["id"]), (self.section, "blocks", "bad"),
            (self.page, "slug", "../atelier"), (self.doc, "menus", [{}]),
            (self.doc, "theme", {"custom": "<raw>"}),
            (self.text["definition"], "version", True),
            (self.text, "children", [copy.deepcopy(self.heading)]),
        ]:
            previous = mapping[key]
            mapping[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValidationError):
                self.check()
            mapping[key] = previous
        self.doc["schema_version"] = 5
        with self.assertRaises(ValidationError) as error:
            self.check()
        self.assertEqual(error.exception.code, "incompatible_schema")

    def test_tree_validation_allows_forward_parents_but_not_cycles_or_slug_collisions(self):
        self.doc["pages"].reverse()
        self.check()
        other = {**self.page, "id": str(uuid4())}
        self.doc["pages"].append(other)
        with self.assertRaises(ValidationError):
            self.check()
        other["slug"] = "autre"
        other["parent_id"] = self.page["id"]
        self.page["parent_id"] = other["id"]
        with self.assertRaises(ValidationError):
            self.check()
        self.page["parent_id"] = str(uuid4())
        with self.assertRaises(ValidationError):
            self.check()

    def test_responsive_overrides_are_independent(self):
        self.section["layout"]["tablet"] = {"gap": 0}
        self.check()
        del self.section["layout"]["mobile"]["columns"]
        with self.assertRaises(ValidationError):
            self.check()

    def test_scoped_reference_providers_and_safe_errors(self):
        self.text["definition"] = {"scope":"site", "key":"photo", "version":2}
        resource = str(uuid4())
        def resolve_definition(site_id, scope, key, version):
            if (site_id, scope, key, version) == (self.site, "site", "photo", 2):
                return {"source": kind}
        def resolve_reference(site_id, actual_kind, ref_id):
            return (site_id, actual_kind, ref_id) == (self.site, kind, resource)
        for kind in ("media", "wagtail_content"):
            self.text["props"] = {"source": {"kind":kind, "ref_id":resource}}
            with self.assertRaises(ValidationError):
                self.check()
            self.check(resolve_definition=resolve_definition, resolve_reference=resolve_reference)
            for missing in (None, lambda *args: False):
                with self.assertRaises(ValidationError) as error:
                    self.check(resolve_definition=resolve_definition, resolve_reference=missing)
                self.assertNotIn(resource, str(error.exception))
            with self.assertRaises(ValidationError):
                check_document(self.doc, uuid4(), resolve_definition=resolve_definition,
                               resolve_reference=resolve_reference)

    def test_page_and_block_depth_limits(self):
        for n in range(11):
            last = self.doc["pages"][-1]
            self.doc["pages"].append({**self.page, "parent_id": last["id"], "id": str(uuid4())})
        with self.assertRaises(ValidationError):
            self.check()
        self.doc["pages"].pop()
        self.check()
        nodes = self.section["blocks"]
        nodes.clear()
        for n in range(12):
            item = {"id": str(uuid4()), "definition": {"scope":"global", "key":"container", "version":1},
                    "props": {"layout":{"base":{}}}, "children":[]}
            nodes.append(item)
            nodes = item["children"]
        self.check()
        nodes.append(self.text)
        with self.assertRaises(ValidationError):
            self.check()

    def test_exact_page_and_node_limits(self):
        while len(self.doc["pages"]) < 100:
            self.doc["pages"].append({**self.page, "id":str(uuid4()), "slug":str(len(self.doc["pages"]))})
        self.check()
        self.doc["pages"].append({**self.page, "id":str(uuid4()), "slug":"extra"})
        with self.assertRaises(ValidationError):
            self.check()
        self.doc["pages"].pop()
        self.section["blocks"] = [{**self.text, "id":str(uuid4())} for _ in range(1999)]
        self.check()
        self.section["blocks"].append({**self.text, "id":str(uuid4())})
        with self.assertRaises(ValidationError):
            self.check()

    def test_exact_compact_utf8_byte_limit(self):
        self.section["blocks"] = [
            {**self.text, "id":str(uuid4()), "props":{"text":"é"*2000}} for _ in range(250)]
        def length():
            return len(json.dumps(self.doc, separators=(",",":"), ensure_ascii=False).encode())
        remaining = 1048576 - length()
        self.assertGreater(remaining, 0)
        for block in self.section["blocks"]:
            take = min(remaining, 2000)
            block["props"]["text"] += "x"*take
            remaining -= take
            if remaining == 0:
                break
        self.assertEqual(length(), 1048576)
        self.check()
        self.root["title"] += "x"
        with self.assertRaises(ValidationError):
            self.check()

    def test_oversized_raw_rejected_before_parser_and_scope_resolution(self):
        raw = json.dumps(self.doc).encode()
        exact = raw + b" " * (4 * 1048576 - len(raw))
        self.assertEqual(self.check(exact), self.doc)
        resolver = Mock()
        with patch("composition.validation.json.loads", side_effect=AssertionError("unexpected parsing")):
            for payload in (exact + b" ", exact.decode() + " ", "é" * (2 * 1048576 + 1)):
                with self.assertRaises(ValidationError):
                    self.check(payload, resolve_definition=resolver)
        resolver.assert_not_called()

    def test_oversized_document_rejected_before_resolving_definitions(self):
        self.text["definition"] = {"scope": "site", "key": "test", "version": 1}
        self.text["props"] = {"text": "é" * 4000}
        self.section["blocks"] = [
            {**self.text, "id": str(uuid4())} for _ in range(140)]
        resolver = Mock(return_value={"text": "text"})
        with self.assertRaises(ValidationError):
            self.check(resolve_definition=resolver)
        resolver.assert_not_called()
