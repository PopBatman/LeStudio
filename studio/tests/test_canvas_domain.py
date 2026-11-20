from copy import deepcopy
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404

from composition.appearance import modifier_apparence
from composition.catalogue import attribuer_media
from composition.editor import creer_atelier, modifier_structure
from composition.models import ComponentVersion
from composition.placement import effective_placement
from composition.services import (ScopedComposition, creer_brouillon, lire_brouillon, lire_revision,
                                  modifier_navigation)
from composition.validation import check_document
from registre.models import Client, Site, SiteGrant
from registre.services import Conflict
from tests.catalogue_fixture import CatalogueTestCase
from workspace.access import OPERATOR_GROUP


class CanvasDomainTests(CatalogueTestCase):
    def setUp(self):
        self.actor = User.objects.create_user("Gestion")
        self.actor.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        client = Client.objects.create(client_type="COMPANY", display_name="Exemple")
        self.site = Site.objects.create(client=client, name="Atelier")
        self.grant = SiteGrant.objects.create(user=self.actor, site=self.site, level="manage")
        self.head = creer_atelier(self.actor, self.site.pk, "template")
        self.initial = deepcopy(self.head)
        page = self.head["document"]["pages"][0]
        self.page = page["id"]
        self.section = page["sections"][0]["id"]
        self.block = page["sections"][0]["blocks"][0]["id"]
        self.free = dict(mode="free", x=10, width=60, y=16, height=112, z=2)

    def apply(self, action, **fields):
        self.head, selected = modifier_structure(self.actor, self.site.pk, self.head["id"],
                                                {"action": action, "page": self.page, **fields})
        return selected

    def place(self, fmt, patch, **kwargs):
        return self.apply("block_place", id=self.block, format=fmt, patch=patch, **kwargs)

    def saved_placement(self):
        return self.head["document"]["pages"][0]["sections"][0]["blocks"][0]["placement"]

    def test_persistence_and_inheritance_between_modes_and_formats(self):
        self.assertEqual(self.place("mobile", {}, clear=["x"]), self.block)
        self.assertEqual(self.head, self.initial)
        self.place("base", self.free)
        self.assertEqual((self.head["number"], self.head["schema_version"]), (2, 4))
        self.place("tablet", {"x": 5, "width": 60})
        self.place("mobile", {"mode": "flow"})
        placement = self.saved_placement()
        self.assertEqual(effective_placement(placement, "mobile"), {"mode": "flow", "span": 1})
        self.place("base", {"width": 42})
        self.assertEqual(effective_placement(self.saved_placement(), "tablet")["width"], 60)
        self.place("tablet", {}, clear=["width"])
        self.assertEqual(self.saved_placement()["tablet"], {"x": 5})
        self.assertEqual(effective_placement(self.saved_placement(), "tablet")["width"], 42)
        self.assertEqual(lire_revision(self.actor, self.site.pk, self.initial["id"]), self.initial)

    def test_other_writers_keep_v4(self):
        self.place("base", self.free)
        self.head = modifier_apparence(self.actor, self.site.pk, self.head["id"],
                                      {"action": "theme", "values": {"gap": 22}})
        self.head = modifier_navigation(self.actor, self.site.pk, self.head["id"],
                                      {"action": "menu_add", "label": "Menu"})
        self.apply("block_edit", id=self.block, definition={"scope": "global", "key": "heading", "version": 1},
                   props={"text": "Titre édité", "level": 2})
        self.assertEqual(self.saved_placement(), {"base": self.free})
        self.assertEqual(self.head["schema_version"], 4)

    def test_span_and_parent_layout_all_formats_atomic(self):
        self.apply("parent_layout", id=self.section, format="base", patch={"display": "grid", "columns": 3})
        self.place("base", {"span": 3})
        with self.assertRaises(ValidationError):
            self.apply("parent_layout", id=self.section, format="tablet", patch={"columns": 2})
        self.place("tablet", {"span": 1})
        self.apply("parent_layout", id=self.section, format="tablet", patch={"columns": 2})
        new = self.apply("section_add")
        with self.assertRaises(ValidationError):
            self.place("base", {}, parent=new)
        self.place("base", {"span": 1}, parent=new)
        saved = self.head["document"]["pages"][0]["sections"][-1]["blocks"][0]
        self.assertEqual(saved["id"], self.block)

    def test_invalid_patches_and_stale_base_leave_revision_intact(self):
        for bad in ({"x": 41}, {"width": True}, {"height": 1.0}, {"y": 4000}, {"css": "fixed"}):
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                self.place("base", {**self.free, **bad})
        self.place("base", self.free)
        with self.assertRaises(Conflict):
            modifier_structure(self.actor, self.site.pk, self.initial["id"], {
                "action": "block_place", "page": self.page, "id": self.block, "format": "base", "patch": {"z": 9}})
        with self.assertRaises(ValidationError):
            self.place("mobile", {}, parent=str(uuid4()))
        self.grant.level = "read"
        self.grant.save()
        with self.assertRaises(PermissionDenied):
            self.place("base", {"z": 2})
        self.assertEqual(lire_brouillon(self.actor, self.site.pk), self.head)
        self.grant.delete()
        with self.assertRaises(Http404):
            self.place("base", {})

    def test_private_v4_source_and_version_boundary(self):
        self.place("base", self.free)
        source = deepcopy(self.head["document"])
        other = Site.objects.create(client=self.site.client, name="Autre")
        SiteGrant.objects.create(user=self.actor, site=other, level="manage")
        media = attribuer_media(other)
        source["theme"]["media"] = {"kind": "media", "ref_id": str(media.pk)}
        origin = {"kind": "template", "ref": "exemple", "version": "1"}
        with self.assertRaises(ValidationError):
            creer_brouillon(self.actor, other.pk, origin, resolve_origin=lambda *_: ScopedComposition(self.site.pk, source))
        result = creer_brouillon(self.actor, other.pk, origin, resolve_origin=lambda *_: ScopedComposition(other.pk, source))
        self.assertNotEqual(result["document"]["pages"][0]["id"], self.page)
        self.assertEqual(result["document"]["pages"][0]["sections"][0]["blocks"][0]["placement"], {"base": self.free})
        with self.assertRaises(ValidationError):
            check_document({**source, "schema_version": 3}, other.pk)

    def test_nested_free_geometry_and_opaque_content_are_validated(self):
        box = self.apply("block_add", parent=self.section,
                         definition={"scope": "global", "key": "container", "version": 1},
                         props={"layout": {"base": {"display": "stack"}}})
        self.apply("block_place", id=box, format="base", patch={**self.free, "height": 80})
        with self.assertRaises(ValidationError):
            self.place("base", self.free, parent=box)
        self.place("base", {**self.free, "height": 64}, parent=box)
        previous = self.head
        with self.assertRaises(ValidationError):
            self.apply("block_place", id=box, format="mobile", patch={"height": 79})
        self.assertEqual(lire_brouillon(self.actor, self.site.pk), previous)
        ComponentVersion.objects.filter(key="heading").delete()
        with self.assertRaises(ValidationError):
            self.place("mobile", {"z": 101})
        self.place("mobile", {"z": 3})
        self.assertEqual(self.head["number"], previous["number"] + 1)

    def test_snapshot_normalizes_only_empty_overrides_without_mutating_input(self):
        self.place("base", self.free)
        source = deepcopy(self.head["document"])
        value = source["pages"][0]["sections"][0]["blocks"][0]["placement"]
        value.update(tablet={}, mobile={"z": 2})
        checked = check_document(source, self.site.pk)
        self.assertIn("tablet", value)
        self.assertEqual(checked["pages"][0]["sections"][0]["blocks"][0]["placement"],
                         {"base": self.free, "mobile": {"z": 2}})

    def test_legacy_text_property_named_layout_is_not_a_container(self):
        from composition.catalogue import installer_version
        other = Site.objects.create(client=self.site.client, name="Archives")
        SiteGrant.objects.create(user=self.actor, site=other, level="manage")
        source = deepcopy(self.initial["document"])
        node = source["pages"][0]["sections"][0]["blocks"][0]
        node.update(definition={"scope": "site", "key": "archives", "version": 1},
                    props={"layout": "Ancienne disposition"})
        source["schema_version"] = 1
        first = creer_brouillon(self.actor, other.pk, {"kind": "blank"}, source,
                                resolve_definition=lambda *_: {"layout": "text"})
        installer_version(other, "archives", 1, "Archives", "container")
        for command in [
            {"action": "parent_layout", "id": node["id"], "format": "base", "patch": {"gap": 12}},
            {"action": "block_add", "parent": node["id"], "definition": {"scope": "global", "key": "text", "version": 1},
             "props": {"text": "Enfant"}},
        ]:
            with self.subTest(command=command), self.assertRaises(ValidationError):
                modifier_structure(self.actor, other.pk, first["id"], {"page": self.page, **command})
            self.assertEqual(lire_brouillon(self.actor, other.pk), first)
        saved, _ = modifier_structure(self.actor, other.pk, first["id"], {
            "page": self.page, "id": node["id"], "action": "block_place", "format": "base", "patch": self.free})
        self.assertEqual(saved["document"]["pages"][0]["sections"][0]["blocks"][0]["props"], node["props"])
