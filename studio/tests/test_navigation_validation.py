from copy import deepcopy
import unittest
from uuid import uuid4

from django.core.exceptions import ValidationError

from composition.validation import check_document, remap_occurrence_ids


def entry(label, target, parent=None):
    return {"id": str(uuid4()), "parent_id": parent, "label": label, "target": target,
            "visibility": ["desktop", "tablet", "mobile"]}


class NavigationValidationTests(unittest.TestCase):
    def setUp(self):
        self.site = uuid4()
        self.root = {"id": str(uuid4()), "parent_id": None, "title": "Accueil", "slug": "", "sections": []}
        self.group = entry("Annuaire", {"kind": "group"})
        self.link = entry("Site", {"kind": "page", "page_id": self.root["id"]}, self.group["id"])
        self.external = entry("Billetterie", {"kind": "external", "url": "https://tickets.example.org/p?x=3#ici"})
        self.menu = {"id": str(uuid4()), "label": "Principal", "items": [self.link, self.group, self.external]}
        self.footer = {"id": str(uuid4()), "label": "Pied", "items": []}
        self.doc = {"schema_version": 2, "pages": [self.root], "theme": {}, "menus": [self.menu, self.footer]}

    def check(self, doc=None):
        return check_document(self.doc if doc is None else doc, self.site)

    def test_copy_preserves_forward_references_external_urls_and_order(self):
        original = deepcopy(self.doc)
        self.assertEqual(self.check(), original)
        copied = remap_occurrence_ids(self.doc)
        self.assertEqual(self.check(copied), copied)
        self.assertEqual(self.doc, original)
        menu, footer = copied["menus"]
        link, group, external = menu["items"]
        self.assertEqual(link["parent_id"], group["id"])
        self.assertEqual(link["target"]["page_id"], copied["pages"][0]["id"])
        self.assertEqual(external["target"], self.external["target"])
        self.assertEqual(link["visibility"], self.link["visibility"])
        for src, dest in zip([self.link, self.group, self.external, self.menu, self.footer, self.root],
                             [link, group, external, menu, footer, copied["pages"][0]]):
            self.assertNotEqual(src["id"], dest["id"])

    def test_integrity_errors_report_invalid_document(self):
        cases = [
            (self.group, "parent_id", self.link["id"]),
            (self.menu, "id", self.root["id"]),
            (self.link, "id", self.menu["id"]),
            (self.link, "parent_id", self.footer["id"]),
            (self.link, "target", {"kind": "page", "page_id": self.group["id"]}),
            (self.link, "target", {"kind": "page", "page_id": []}),
            (self.link, "target", {"kind": "group", "url": "extra"}),
            (self.link, "target", {"kind": "typo"}),
            (self.link, "label", "  "),
            (self.link, "visibility", ["desktop", []]),
            (self.link, "visibility", ["desktop", "desktop"]),
            (self.link, "visibility", []),
        ]
        for node, key, value in cases:
            previous = node[key]
            node[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValidationError) as caught:
                self.check()
            self.assertEqual(caught.exception.code, "invalid_document")
            node[key] = previous
        self.footer["items"].append(self.menu["items"].pop(0))
        with self.assertRaises(ValidationError):
            self.check()

    def test_external_destination_policy(self):
        target = self.external["target"]
        for url in ("https://xn--caf-dma.example:8443/places", "https://example.org/"):
            target["url"] = url
            self.check()
        for url in ("http://tickets.example", "/relative", "https://a@tickets.example",
                    "https://tickets.example:99999", "https://tickets.example:",
                    "https://tickets.example/a\nb", "https://tickets.example/a\\b",
                    "https://bad_host.example", "https://[v1.foo]/", "https://bad..example", "https://café.example/",
                    "https://example.org/" + "x" * 2048):
            target["url"] = url
            with self.subTest(url=url), self.assertRaises(ValidationError):
                self.check()

    def test_count_and_depth_boundaries(self):
        self.menu["items"] = [entry("Groupe", {"kind": "group"}) for _ in range(6)]
        for parent, child in zip(self.menu["items"], self.menu["items"][1:]):
            child["parent_id"] = parent["id"]
        self.check()
        self.menu["items"].append(entry("Trop profond", {"kind": "group"}, self.menu["items"][-1]["id"]))
        with self.assertRaises(ValidationError):
            self.check()
        self.menu["items"] = [entry("Groupe", {"kind": "group"}) for _ in range(500)]
        self.check()
        self.footer["items"].append(self.group)
        with self.assertRaises(ValidationError):
            self.check()
        self.doc["menus"] = [dict(id=str(uuid4()), label="Vide", items=[]) for _ in range(20)]
        self.check()
        self.doc["menus"].append(self.footer)
        with self.assertRaises(ValidationError):
            self.check()
