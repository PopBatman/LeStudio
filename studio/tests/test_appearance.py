from copy import deepcopy
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError

from composition.appearance import diagnostics, effective_appearance, modifier_apparence
from composition.services import (
    creer_brouillon,
    enregistrer_brouillon,
    lire_revision,
    modifier_navigation,
)
from composition.models import CompositionRevision
from registre.models import Client, Site, SiteGrant
from registre.services import Conflict
from tests.catalogue_fixture import CatalogueTestCase
from workspace.access import OPERATOR_GROUP


class AppearanceTests(CatalogueTestCase):
    def setUp(self):
        self.user = User.objects.create_user("Gestion")
        self.user.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        client = Client.objects.create(client_type="COMPANY", display_name="Exemple")
        self.site = Site.objects.create(client=client, name="Atelier")
        SiteGrant.objects.create(user=self.user, site=self.site, level="manage")
        self.first = creer_brouillon(self.user, self.site.pk, {"kind": "blank"})
        self.root = self.first["document"]["pages"][0]["id"]
        self.head = self.first

    def change(self, **command):
        self.head = modifier_apparence(self.user, self.site.pk, self.head["id"], command)
        return self.head

    def block(self, key="button"):
        return {
            "id": str(uuid4()),
            "definition": {"scope": "global", "key": key, "version": 1},
            "props": {"label": "Programme", "url": "https://example.org/"},
            "children": [],
        }

    def store(self, *blocks):
        doc = deepcopy(self.head["document"])
        doc["schema_version"] = 3
        doc["pages"][0]["sections"] = [
            {"id": str(uuid4()), "layout": {"base": {}}, "blocks": list(blocks)}
        ]
        self.head = enregistrer_brouillon(self.user, self.site.pk, self.head["id"], doc)

    def test_upgrade_navigation_noop_old_revision_and_stale_conflict(self):
        self.assertEqual(self.change(action="theme", values={}), self.first)
        self.change(action="theme", values={"gap": 4, "font": "dm-sans"})
        saved = modifier_navigation(
            self.user, self.site.pk, self.head["id"], {"action": "menu_add", "label": "Pied"}
        )
        self.assertEqual(saved["schema_version"], 3)
        self.assertEqual(saved["document"]["theme"], self.head["document"]["theme"])
        self.assertEqual(lire_revision(self.user, self.site.pk, self.first["id"]), self.first)
        with self.assertRaises(Conflict):
            self.change(action="theme", values={"gap": 5})
        with self.assertRaises(ValidationError):
            enregistrer_brouillon(self.user, self.site.pk, saved["id"], self.first["document"])

    def test_preferences_and_strict_types(self):
        block = self.block()
        self.store(block)
        self.change(action="theme", values={"gap": 16})
        self.change(
            action="preference", definition=block["definition"], appearance={"tokens": {"gap": 12}}
        )
        self.change(
            action="block",
            id=block["id"],
            definition=block["definition"],
            props=block["props"],
            appearance={"tokens": {"gap": 8}, "variant": "secondary"},
        )
        doc = self.head["document"]
        stored = doc["pages"][0]["sections"][0]["blocks"][0]
        self.assertEqual(
            effective_appearance(
                doc["theme"], stored, {"variants": ["primary", "secondary"], "tokens": ["gap"]}
            ),
            {"tokens": {"gap": 8}, "variant": "secondary"},
        )
        self.assertFalse(diagnostics(self.site.pk, doc))
        for values in (
            {"gap": True},
            {"font": "url()"},
            {"media": {"kind": "media", "ref_id": str(uuid4())}},
        ):
            with self.assertRaises(ValidationError):
                self.change(action="theme", values=values)

    def test_partial_repair_keeps_other_invalid_occurrence(self):
        blocks = [self.block(), self.block()]
        self.store(*blocks)
        doc = deepcopy(self.head["document"])
        for b in doc["pages"][0]["sections"][0]["blocks"]:
            b["definition"]["version"] = 71
        CompositionRevision.objects.filter(pk=self.head["id"]).update(document=doc)
        self.assertEqual(len(diagnostics(self.site.pk, doc)), 2)
        self.change(
            action="block",
            id=blocks[0]["id"],
            definition=blocks[0]["definition"],
            props=blocks[0]["props"],
            appearance={},
        )
        self.assertEqual(len(diagnostics(self.site.pk, self.head["document"])), 1)
        with self.assertRaises(ValidationError):
            enregistrer_brouillon(self.user, self.site.pk, self.head["id"], self.head["document"])
        self.change(action="remove", id=blocks[1]["id"], confirmed=True)
        self.assertFalse(diagnostics(self.site.pk, self.head["document"]))

    def test_unavailable_renderer_and_explicit_reset_of_missing_preference(self):
        from composition.models import ComponentVersion

        block = self.block()
        self.store(block)
        self.change(
            action="preference", definition=block["definition"], appearance={"variant": "primary"}
        )
        ComponentVersion.objects.filter(site=None, key="button", version=1).update(
            renderer="non_distribue"
        )
        issues = diagnostics(self.site.pk, self.head["document"])
        self.assertEqual(len(issues), 2)
        self.assertTrue(all(i["blocking"] for i in issues))
        with self.assertRaises(ValidationError):
            enregistrer_brouillon(self.user, self.site.pk, self.head["id"], self.head["document"])
        self.change(action="preference", definition=block["definition"], appearance={})
        self.assertEqual(len(diagnostics(self.site.pk, self.head["document"])), 1)

    def test_retired_pin_can_be_kept_but_not_added_again(self):
        from composition.models import ComponentVersion

        block = self.block()
        self.store(block)
        ComponentVersion.objects.filter(site=None, key="button", version=1).update(retired=True)
        (issue,) = diagnostics(self.site.pk, self.head["document"])
        self.assertFalse(issue["blocking"])
        doc = deepcopy(self.head["document"])
        doc["pages"][0]["sections"][0]["blocks"].append(self.block())
        with self.assertRaises(ValidationError):
            enregistrer_brouillon(self.user, self.site.pk, self.head["id"], doc)
        self.change(
            action="block",
            id=block["id"],
            definition=block["definition"],
            props={**block["props"], "label": "Réserver"},
            appearance={},
        )

    def test_private_media_copy_requires_trusted_site_and_rechecks_revocation(self):
        from composition.catalogue import attribuer_media
        from composition.services import ScopedComposition

        other = Site.objects.create(client=self.site.client, name="Autre")
        SiteGrant.objects.create(user=self.user, site=other, level="manage")
        media = attribuer_media(other)
        ref = {"kind": "media", "ref_id": str(media.pk)}
        self.assertFalse(diagnostics(other.pk, {"theme": {"media": ref}, "pages": []}))
        with self.assertRaises(ValidationError):
            self.change(action="theme", values={"media": ref})
        doc = {**self.first["document"], "schema_version": 3, "theme": {"media": ref}}
        origin = {"kind": "template", "ref": "exemple", "version": "1"}
        for source in (doc, ScopedComposition(self.site.pk, doc)):
            with self.assertRaises(ValidationError):
                creer_brouillon(self.user, other.pk, origin, resolve_origin=lambda *_: source)
        saved = creer_brouillon(
            self.user, other.pk, origin, resolve_origin=lambda *_: ScopedComposition(other.pk, doc)
        )
        self.assertNotEqual(saved["document"]["pages"][0]["id"], self.root)
        attribuer_media(other, actif=False)
        self.assertTrue(diagnostics(other.pk, saved["document"])[0]["blocking"])
