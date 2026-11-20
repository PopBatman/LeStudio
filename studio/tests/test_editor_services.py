from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404

from composition.editor import creer_atelier, modifier_structure
from composition.models import ComponentVersion, CompositionRevision
from composition.services import creer_brouillon, lire_revision, modifier_navigation
from registre.models import Client, Site, SiteGrant
from registre.services import Conflict
from tests.catalogue_fixture import CatalogueTestCase
from workspace.access import OPERATOR_GROUP


def definition(key):
    return {"scope": "global", "key": key, "version": 1}


class EditorServicesTests(CatalogueTestCase):
    def setUp(self):
        self.actor = User.objects.create_user("Gestion")
        self.actor.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        self.client_record = Client.objects.create(client_type="COMPANY", display_name="Exemple")
        self.site = Site.objects.create(client=self.client_record, name="Atelier")
        self.grant = SiteGrant.objects.create(user=self.actor, site=self.site, level="manage")

    def start(self, origin="template"):
        self.head = creer_atelier(self.actor, self.site.pk, origin)
        self.page = self.head["document"]["pages"][0]["id"]
        return self.head["document"]["pages"][0]["sections"]

    def change(self, action, **fields):
        self.head, selected = modifier_structure(self.actor, self.site.pk, self.head["id"],
                                                  {"page": self.page, "action": action, **fields})
        return selected

    def test_blank_and_template_are_local_and_copied(self):
        with self.assertRaises(ValidationError):
            creer_atelier(self.actor, self.site.pk, "figma")
        sections = self.start()
        self.assertEqual(self.head["origin"], {"kind": "template", "ref": "presentation-activite", "version": "1"})
        self.assertEqual(len(sections[0]["blocks"]), 2)
        other = Site.objects.create(client=self.client_record, name="Autre")
        SiteGrant.objects.create(user=self.actor, site=other, level="manage")
        copy = creer_atelier(self.actor, other.pk, "template")
        self.assertNotEqual(self.page, copy["document"]["pages"][0]["id"])
        with self.assertRaises(Conflict):
            creer_atelier(self.actor, self.site.pk, "blank")

    def test_upgrade_concurrency_and_permissions(self):
        self.head = creer_brouillon(self.actor, self.site.pk, {"kind": "blank"})
        self.page = self.head["document"]["pages"][0]["id"]
        old = self.head["id"]
        section = self.change("section_add")
        self.assertEqual((self.head["schema_version"], self.head["parent_id"]), (3, old))
        self.change("section_move", id=section)
        self.assertEqual(self.head["number"], 2)
        with self.assertRaises(Conflict):
            modifier_structure(self.actor, self.site.pk, old, {"action": "section_add", "page": self.page})
        self.grant.level = "read"
        self.grant.save()
        with self.assertRaises(PermissionDenied):
            self.change("section_add")
        self.grant.delete()
        with self.assertRaises(Http404):
            self.change("section_add")

    def test_move_reorder_remove_and_preserve_children(self):
        sections = self.start()
        section = sections[0]["id"]
        a, b = [node["id"] for node in sections[0]["blocks"]]
        other = self.change("section_add", before=section)
        box = self.change("block_add", parent=other, definition=definition("container"), props={"layout": {"base": {}}})
        self.change("block_move", id=a, parent=box)
        self.change("block_move", id=b, parent=box, before=a)
        self.assertEqual(self.change("block_remove", id=b, confirmed=True), a)
        self.assertEqual(self.change("block_remove", id=a, confirmed=True), box)
        self.assertEqual(self.change("section_remove", id=other, confirmed=True), section)
        self.assertEqual(self.change("section_remove", id=section, confirmed=True), self.page)

    def test_invalid_destinations_and_inputs_are_atomic(self):
        section = self.start()[0]
        leaf = section["blocks"][0]["id"]
        base = self.change("block_add", parent=section["id"], definition=definition("container"), props={"layout": {"base": {}}})
        nested = self.change("block_add", parent=base, definition=definition("container"), props={"layout": {"base": {}}})
        for action, fields in [
            ("block_move", {"id": base, "parent": nested}),
            ("block_move", {"id": base, "parent": leaf}),
            ("block_move", {"id": nested, "parent": section["id"], "before": str(uuid4())}),
            ("block_remove", {"id": base, "confirmed": False}),
            ("block_edit", {"id": leaf, "definition": definition("heading"), "props": {"text": "titre", "level": 7}}),
            ("section_edit", {"id": section["id"], "layout": {"base": {"display": "script"}}}),
        ]:
            with self.subTest(action=action, fields=fields), self.assertRaises(ValidationError):
                self.change(action, **fields)
        self.assertEqual(CompositionRevision.objects.filter(site=self.site).count(), 3)

    def test_unknown_container_is_preserved_but_refused_as_a_destination(self):
        section = self.start()[0]
        box = self.change("block_add", parent=section["id"], definition=definition("container"),
                          props={"layout": {"base": {}}})
        heading, text = (node["id"] for node in section["blocks"])
        self.change("block_move", id=text, parent=box)
        ComponentVersion.objects.filter(key="container").delete()
        before = self.head["number"]
        for action, fields in [
            ("block_add", {"definition": definition("text"), "props": {"text": "Ajout"}}),
            ("block_move", {"id": heading}),
        ]:
            with self.subTest(action=action), self.assertRaises(ValidationError):
                self.change(action, parent=box, **fields)
        self.change("block_edit", id=heading, definition=definition("heading"),
                    props={"text": "Nouveau titre", "level": 1})
        self.assertEqual(self.head["number"], before + 1)
        preserved = self.head["document"]["pages"][0]["sections"][0]["blocks"][-1]
        self.assertEqual((preserved["id"], preserved["children"][0]["id"]), (box, text))

    def test_v2_navigation_and_other_page_are_preserved(self):
        first = creer_brouillon(self.actor, self.site.pk, {"kind": "blank"})
        self.page = first["document"]["pages"][0]["id"]
        other = modifier_navigation(self.actor, self.site.pk, first["id"],
                                    {"action": "page_add", "parent_id": self.page, "title": "Guide", "slug": "guide"})
        previous = modifier_navigation(self.actor, self.site.pk, other["id"], {"action": "menu_add", "label": "Principal"})
        self.head = previous
        self.assertEqual(previous["schema_version"], 2)
        section = self.change("section_add")
        self.assertEqual(self.head["document"]["menus"], previous["document"]["menus"])
        self.assertEqual(self.head["document"]["pages"][1], previous["document"]["pages"][1])
        self.assertEqual(lire_revision(self.actor, self.site.pk, previous["id"]), previous)
        self.page = previous["document"]["pages"][1]["id"]
        with self.assertRaises(ValidationError):
            self.change("section_remove", id=section, confirmed=True)

    def test_depth_limit_and_image_reference(self):
        self.assertEqual(self.start("blank"), [])
        section = self.change("section_add")
        parent = section
        for _ in range(12):
            parent = self.change("block_add", parent=parent, definition=definition("container"),
                                 props={"layout": {"base": {}}})
        with self.assertRaises(ValidationError):
            self.change("block_add", parent=parent, definition=definition("text"), props={"text": "Enfant"})
        with self.assertRaises(ValidationError):
            self.change("block_add", parent=section, definition=definition("image"),
                        props={"media": {"kind": "media", "ref_id": str(uuid4())}, "alt": "Illustration"})
