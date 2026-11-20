from copy import deepcopy
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.test import TestCase

from composition.models import CompositionRevision
from composition.navigation import ImpactRequired, page_paths
from composition.services import creer_brouillon, enregistrer_brouillon, lire_revision, modifier_navigation
from registre.models import Client, Site, SiteGrant
from registre.services import Conflict
from workspace.access import OPERATOR_GROUP


class NavigationServicesTests(TestCase):
    def setUp(self):
        self.actor = User.objects.create_user("navigation")
        self.actor.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        client = Client.objects.create(display_name="Maison", client_type="COMPANY")
        self.site = Site.objects.create(client=client, name="Maison")
        self.grant = SiteGrant.objects.create(site=self.site, user=self.actor, level="manage")
        self.first = creer_brouillon(self.actor, self.site.pk, {"kind": "blank"})
        self.head = self.first
        self.root = self.first["document"]["pages"][0]["id"]

    def change(self, command, **options):
        self.head = modifier_navigation(self.actor, self.site.pk, self.head["id"], command, **options)
        return self.head

    def impact(self, command, **options):
        with self.assertRaises(ImpactRequired) as caught:
            self.change(command, **options)
        return caught.exception.impact

    def tree(self):
        self.change(dict(action="page_add", title="Guide", slug="guide", parent_id=self.root))
        parent = self.head["document"]["pages"][-1]["id"]
        self.change(dict(action="page_add", title="Une visite", slug="visite", parent_id=parent))
        child = self.head["document"]["pages"][-1]["id"]
        self.change(dict(action="menu_add", label="Principal"))
        menu = self.head["document"]["menus"][0]["id"]
        for label in ("Visiter", "Encore"):
            self.change(dict(action="item_add", menu_id=menu, parent_id=None, label=label,
                             target={"kind":"page","page_id":child}, visibility=["mobile"]))
        entries = self.head["document"]["menus"][0]["items"]
        return parent, child, menu, [entry["id"] for entry in entries]

    def test_explicit_upgrade_and_noop(self):
        self.change(dict(action="page_edit", id=self.root, title="Accueil", slug=""))
        self.assertEqual(self.head, self.first)
        self.change(dict(action="menu_add", label="Principal"))
        self.assertEqual(self.head["schema_version"], 2)
        self.assertEqual(lire_revision(self.actor, self.site.pk, self.first["id"]), self.first)
        with self.assertRaises(ValidationError):
            enregistrer_brouillon(self.actor, self.site.pk, self.head["id"], self.first["document"])

    def test_recomputed_impact_all_descendants_and_stale_revision(self):
        parent, child, _, entries = self.tree()
        command = dict(action="page_edit", id=parent, title="Guide", slug="programme")
        result = self.impact(command)
        self.assertEqual({p["id"] for p in result["pages"]}, {parent, child})
        self.assertEqual({e["id"] for e in result["entries"]}, set(entries))
        self.assertTrue(result["complete"])
        base = self.head["id"]
        altered = dict(command, slug="autre")
        self.impact(altered, confirmation=result["token"])
        self.change(command, confirmation=result["token"])
        self.assertEqual(page_paths(self.head["document"]["pages"])[child], "/programme/visite/")
        with self.assertRaises(Conflict):
            modifier_navigation(self.actor, self.site.pk, base, command, confirmation=result["token"])

    def test_delete_mixed_decisions_and_full_document_cannot_bypass(self):
        parent, child, menu, entries = self.tree()
        base = self.head
        command = dict(action="page_delete", id=parent)
        unresolved = self.impact(command)
        self.assertFalse(unresolved["complete"])
        decisions = {entries[0]: "remove", entries[1]: self.root}
        ready = self.impact(command, resolutions=decisions)
        self.assertTrue(ready["complete"])
        foreign = deepcopy(base["document"])
        foreign["pages"] = foreign["pages"][:1]
        foreign["menus"][0]["items"].clear()
        with self.assertRaises(ImpactRequired):
            enregistrer_brouillon(self.actor, self.site.pk, base["id"], foreign,
                                  confirmation=ready["token"], resolutions=decisions)
        self.assertEqual(CompositionRevision.objects.count(), base["number"])
        self.change(command, confirmation=ready["token"], resolutions=decisions)
        items = self.head["document"]["menus"][0]["items"]
        self.assertEqual([(i["id"], i["target"]["page_id"]) for i in items], [(entries[1],self.root)])

    def test_impact_after_revoked_grant_and_unknown_site(self):
        parent, _, _, _ = self.tree()
        command = dict(action="page_delete", id=parent)
        self.grant.level = "read"
        self.grant.save()
        with self.assertRaises(PermissionDenied):
            self.change(command)
        with self.assertRaises(Http404):
            modifier_navigation(self.actor, uuid4(), self.head["id"], command)

    def test_navigation_preserves_scoped_blocks_without_resolving_new_references(self):
        doc = deepcopy(self.first["document"])
        reference = str(uuid4())
        block = {"id": str(uuid4()), "definition": {"scope": "site", "key": "photo", "version": 1},
                 "props": {"image": {"kind": "media", "ref_id": reference}}, "children": []}
        sections = [{"id": str(uuid4()), "layout": {"base": {}}, "blocks": [block]}]
        doc["pages"][0]["sections"] = sections
        self.head = enregistrer_brouillon(
            self.actor, self.site.pk, self.first["id"], doc,
            resolve_definition=lambda *args: {"image": "media"},
            resolve_reference=lambda site, kind, ref: site == self.site.pk and ref == reference,
        )
        command = dict(action="page_edit", id=self.root, title="Nouvel accueil", slug="")
        self.change(command)
        self.assertEqual(self.head["document"]["pages"][0]["sections"], sections)
        forged = deepcopy(self.head["document"])
        forged["pages"][0]["sections"][0]["blocks"][0]["props"]["image"]["ref_id"] = str(uuid4())
        with self.assertRaises(ValidationError):
            enregistrer_brouillon(self.actor, self.site.pk, self.head["id"], forged)
        with self.assertRaises(ValidationError):
            self.change(command, resolve_definition=lambda *args: {"image": "media"},
                        resolve_reference=lambda *args: False)

    def test_delete_parent_entry_requires_explicit_handling_of_its_children(self):
        parent, child, menu, entries = self.tree()
        self.change(dict(action="item_move", menu_id=menu, id=entries[1], parent_id=entries[0]))
        command = dict(action="page_delete", id=parent)
        dangling = {entries[0]: "remove", entries[1]: self.root}
        self.assertFalse(self.impact(command, resolutions=dangling)["complete"])
        choices = {entries[0]: "remove", entries[1]: "remove"}
        self.assertFalse(self.impact(command, resolutions=choices)["complete"])
        choices[entries[0]] = "remove_branch"
        ready = self.impact(command, resolutions=choices)
        self.assertTrue(ready["complete"])
        self.assertEqual(len(ready["removed_entries"]), 2)
        self.change(command, resolutions=choices, confirmation=ready["token"])
        self.assertEqual(self.head["document"]["menus"][0]["items"], [])
