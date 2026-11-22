from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import connections
from django.test import TransactionTestCase, skipUnlessDBFeature

from composition.builder_batch import save_batch
from composition.catalogue import attribuer_media
from composition.editor import creer_atelier
from composition.models import BuilderSave, ComponentVersion, CompositionRevision, SiteMedia
from composition.services import creer_brouillon
from registre.models import Client, Site, SiteGrant
from registre.services import Conflict
from tests.catalogue_fixture import CatalogueTestCase
from workspace.access import OPERATOR_GROUP


def uid():
    return str(uuid4())


def definition(key):
    return {"scope": "global", "key": key, "version": 1}


class BatchTests(CatalogueTestCase):
    def setUp(self):
        self.user = User.objects.create_user("graphisme")
        self.user.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        self.site = Site.objects.create(client=Client.objects.create(display_name="Doubs", client_type="COMPANY"),
                                        name="Refuge")
        self.grant = SiteGrant.objects.create(site=self.site, user=self.user, level="manage")
        self.base = creer_atelier(self.user, self.site.pk, "template")
        self.page = self.base["document"]["pages"][0]
        self.section = self.page["sections"][0]
        self.target = self.section["blocks"][0]

    def payload(self, *commands, **options):
        return {"base": self.base["id"], "page": self.page["id"], "key": uid(),
                "commands": list(commands), **options}

    def save(self, payload):
        return save_batch(self.user, self.site.pk, payload)

    def test_new_section_add_edit_one_revision_retry_and_revoked_access(self):
        section, temp = uid(), uid()
        packet = self.payload({"action": "section_add", "local_id": section},
                              {"action": "block_add", "local_id": temp, "parent": section,
                               "definition": definition("text"), "props": {"text": "Premier"}},
                              {"action": "block_edit", "id": temp, "definition": definition("text"),
                               "props": {"text": "Final"}}, selection=temp)
        result = self.save(packet)
        self.assertEqual(result["number"], 2)
        self.assertEqual(result["selection"], result["mapping"][temp])
        node = CompositionRevision.objects.get(pk=result["revision"]).document["pages"][0]["sections"][-1]["blocks"][0]
        self.assertEqual((node["id"], node["props"]), (result["selection"], {"text": "Final"}))
        self.assertEqual(self.save(packet), result)
        with self.assertRaises(ValidationError):
            self.save({**packet, "commands": []})
        with self.assertRaises(Conflict):
            self.save({**packet, "key": uid()})
        self.grant.level = "read"
        self.grant.save()
        with self.assertRaises(PermissionDenied):
            self.save(packet)
        self.assertEqual(CompositionRevision.objects.count(), 2)

    def test_atomic_error_retired_component_and_noop_legacy(self):
        temp = uid()
        cmd = {"action": "block_add", "local_id": temp, "parent": self.section["id"],
               "definition": definition("heading"), "props": {"text": "Titre", "level": 1}}
        with self.assertRaises(ValidationError):
            self.save(self.payload(cmd, {"action": "block_move", "id": temp, "parent": uid()}))
        ComponentVersion.objects.filter(key="heading").update(retired=True)
        with self.assertRaises(ValidationError):
            self.save(self.payload(cmd))
        self.assertEqual(BuilderSave.objects.count(), 0)
        self.assertEqual(CompositionRevision.objects.count(), 1)
        other = Site.objects.create(client=self.site.client, name="Second")
        SiteGrant.objects.create(user=self.user, site=other, level="manage")
        start = creer_brouillon(self.user, other.pk, {"kind": "blank"})
        packet = {"base": start["id"], "page": start["document"]["pages"][0]["id"], "key": uid(),
                  "commands": [{"action": "section_add", "local_id": temp},
                               {"action": "section_remove", "id": temp, "confirmed": True}]}
        self.assertEqual(save_batch(self.user, other.pk, packet)["revision"], start["id"])

    def test_media_and_buttons_are_validated_in_the_current_site(self):
        other = Site.objects.create(client=self.site.client, name="Autre site")
        foreign = attribuer_media(other)
        asset = attribuer_media(self.site)
        def image(media):
            return {"action": "block_add", "parent": self.section["id"], "local_id": uid(),
                    "definition": definition("image"),
                    "props": {"media": {"kind": "media", "ref_id": str(media.pk)}, "alt": "Paysage"}}
        def button(url):
            return {"action": "block_add", "parent": self.section["id"], "local_id": uid(),
                    "definition": definition("button"), "props": {"label": "Découvrir", "url": url}}
        with self.assertRaises(ValidationError):
            self.save(self.payload(image(foreign)))
        with self.assertRaises(ValidationError):
            self.save(self.payload(image(asset), button("Destination inconnue")))
        packet = self.payload(image(asset), button("https://studio.example/"))
        SiteMedia.objects.filter(pk=asset.pk).update(active=False)
        with self.assertRaises(ValidationError):
            self.save(packet)
        self.assertEqual(CompositionRevision.objects.count(), 1)
        SiteMedia.objects.filter(pk=asset.pk).update(active=True)
        self.assertEqual(self.save(packet)["number"], 2)

    def test_recursive_copy_maps_descendants_and_rejects_cycle(self):
        parent, child, copy, copied_child = (uid() for _ in range(4))
        add = {"action": "block_add", "parent": self.section["id"], "local_id": parent,
               "definition": definition("container"), "props": {"layout": {"base": {}}}}
        move = {"action": "block_add", "parent": parent, "local_id": child, "definition": definition("text"),
                "props": {"text": "Copie"}}
        duplicate = {"action": "block_duplicate", "id": parent, "local_ids": {parent: copy, child: copied_child}}
        with self.assertRaises(ValidationError):
            self.save(self.payload(add, move, duplicate, {"action": "block_move", "id": copy, "parent": copied_child}))
        result = self.save(self.payload(add, move, duplicate))
        last = CompositionRevision.objects.get(pk=result["revision"]).document["pages"][0]["sections"][0]["blocks"][-2:]
        self.assertEqual([b["children"][0]["id"] for b in last],
                         [result["mapping"][child], result["mapping"][copied_child]])
        self.assertEqual(len(set(result["mapping"].values())), 4)

    def test_new_collision_refused_unless_intentional_free_layer(self):
        a, b = self.section["blocks"][:2]
        place = {"action": "block_place", "format": "base",
                 "patch": {"mode": "free", "x": 0, "y": 10, "width": 40, "height": 40, "z": 2}}
        first, second = {**place, "id": a["id"]}, {**place, "id": b["id"]}
        with self.assertRaises(ValidationError):
            self.save(self.payload(first, second))
        saved = self.save(self.payload(first, {**second, "overlap": True,
                                               "patch": {**second["patch"], "z": 3}}))
        self.assertEqual(saved["number"], 2)
        for intention in (True, False):
            with self.subTest(overlap=intention), self.assertRaises(ValidationError) as error:
                self.save(self.payload({**second, "patch": {"z": 2}, "overlap": intention},
                                       base=saved["revision"]))
            self.assertEqual(error.exception.code, "collision")
        self.assertEqual(CompositionRevision.objects.count(), 2)


    def _free_pair(self):
        a, b = self.section["blocks"][:2]
        basic = {
            "action": "block_place", "format": "base",
            "patch": {"mode": "free", "y": 12, "width": 40, "height": 80, "z": 0},
        }
        first = self.save(self.payload(
            {**basic, "id": a["id"], "patch": {**basic["patch"], "x": 0}},
            {**basic, "id": b["id"], "patch": {**basic["patch"], "x": 55}},
        ))
        return a["id"], b["id"], first

    def test_grouped_swap_checks_only_final_positions_and_saves_once(self):
        a, b, first = self._free_pair()
        intent = self.payload({
            "action": "gesture_group",
            "steps": [
                {"action": "block_place", "id": a, "format": "base", "patch": {"x": 55}},
                {"action": "block_place", "id": b, "format": "base", "patch": {"x": 0}},
            ],
        }, base=first["revision"])
        result = self.save(intent)
        self.assertEqual(result["number"], first["number"] + 1)
        self.assertEqual(result["selection"], b)
        self.assertEqual(self.save(intent), result)
        self.assertEqual(BuilderSave.objects.count(), 2)
        self.assertEqual(CompositionRevision.objects.count(), 3)
        previous = CompositionRevision.objects.get(pk=first["revision"]).document
        current = CompositionRevision.objects.get(pk=result["revision"]).document
        earlier = previous["pages"][0]["sections"][0]["blocks"][:2]
        revised = current["pages"][0]["sections"][0]["blocks"][:2]
        self.assertEqual([n["placement"]["base"]["x"] for n in earlier], [0, 55])
        self.assertEqual([n["placement"]["base"]["x"] for n in revised], [55, 0])
        self.assertEqual([n["id"] for n in revised], [a, b])
        self.grant.level = "read"
        self.grant.save()
        with self.assertRaises(PermissionDenied):
            self.save(intent)

    def test_group_with_invalid_final_collision_rolls_back_all_steps(self):
        a, b, first = self._free_pair()
        command = {"action": "gesture_group", "steps": [
            {"action": "block_place", "id": a, "format": "base", "patch": {"x": 55}},
            {"action": "block_place", "id": b, "format": "base", "patch": {"x": 55}},
        ]}
        with self.assertRaises(ValidationError) as error:
            self.save(self.payload(command, base=first["revision"]))
        self.assertEqual(error.exception.code, "collision")
        self.assertEqual(CompositionRevision.objects.count(), 2)
        self.assertEqual(BuilderSave.objects.count(), 1)

    def test_group_limits_and_forbidden_steps_preserve_history(self):
        a, b = [n["id"] for n in self.section["blocks"][:2]]
        step = {"action": "block_place", "id": a, "format": "base", "patch": {"width": 50}}
        other = {**step, "id": b}
        attempts = [
            {"action": "gesture_group", "steps": [step]},
            {"action": "gesture_group", "steps": [step] * 9},
            {"action": "gesture_group", "steps": [step, step]},
            {"action": "gesture_group", "steps": [step, {
                "action": "block_remove", "id": b, "confirmed": True,
            }]},
            {"action": "gesture_group", "steps": [step, {
                "action": "gesture_group", "steps": [other, step],
            }]},
            {"action": "gesture_group", "steps": [step, other], "extra": True},
        ]
        for candidate in attempts:
            with self.subTest(candidate=candidate), self.assertRaises(ValidationError):
                self.save(self.payload(candidate))
        with self.assertRaises(ValidationError):
            self.save(self.payload(*([
                {"action": "gesture_group", "steps": [step, other]}
            ] * 65)))
        self.assertEqual(BuilderSave.objects.count(), 0)
        self.assertEqual(CompositionRevision.objects.count(), 1)

    def test_group_reparents_a_block_and_preserves_every_occurrence_id(self):
        a, b, first = self._free_pair()
        local_section = uid()
        created = self.save(self.payload(
            {"action": "section_add", "local_id": local_section},
            base=first["revision"],
        ))
        second_section = created["mapping"][local_section]
        moved = self.save(self.payload({
            "action": "gesture_group",
            "steps": [
                {"action": "block_place", "id": a, "format": "base",
                 "patch": {}, "parent": second_section, "before": None},
                {"action": "block_place", "id": b, "format": "base",
                 "patch": {"x": 0}, "parent": self.section["id"], "before": None},
            ],
        }, base=created["revision"]))
        sections = CompositionRevision.objects.get(
            pk=moved["revision"],
        ).document["pages"][0]["sections"]
        self.assertEqual(
            [n["id"] for n in sections[0]["blocks"] if n["id"] in (a, b)], [b],
        )
        self.assertEqual([n["id"] for n in sections[-1]["blocks"]], [a])
        self.assertEqual(CompositionRevision.objects.count(), 4)
        with self.assertRaises(ValidationError):
            self.save(self.payload({
                "action": "gesture_group",
                "steps": [
                    {"action": "block_place", "id": a, "format": "base",
                     "patch": {}, "parent": uid()},
                    {"action": "block_place", "id": b, "format": "base",
                     "patch": {"width": 38}},
                ],
            }, base=moved["revision"]))
        self.assertEqual(CompositionRevision.objects.count(), 4)

    def test_group_failure_rolls_back_other_commands_in_same_batch(self):
        a, b = [n["id"] for n in self.section["blocks"][:2]]
        packet = self.payload(
            {"action": "section_add", "local_id": uid()},
            {"action": "gesture_group", "steps": [
                {"action": "block_place", "id": a, "format": "base",
                 "patch": {"mode": "free", "x": 95, "y": 0, "width": 40, "height": 50}},
                {"action": "block_place", "id": b, "format": "base",
                 "patch": {"mode": "free", "x": 0, "y": 0, "width": 20, "height": 50}},
            ]},
        )
        with self.assertRaises(ValidationError):
            self.save(packet)
        self.assertEqual(CompositionRevision.objects.count(), 1)
        self.assertEqual(BuilderSave.objects.count(), 0)


@skipUnlessDBFeature("has_select_for_update")
class BatchConcurrencyTests(TransactionTestCase):
    def test_simultaneous_retry_and_distinct_stale_request(self):
        client = Client.objects.create(display_name="Deux gestionnaires", client_type="COMPANY")
        site = Site.objects.create(client=client, name="Atlas")
        group = Group.objects.create(name=OPERATOR_GROUP)
        users = [User.objects.create_user(name) for name in ("est", "ouest")]
        for actor in users:
            actor.groups.add(group)
            SiteGrant.objects.create(site=site, user=actor, level="manage")
        base = creer_atelier(users[0], site.pk, "blank")
        def packet(base):
            return {"base": base, "page": page, "key": uid(),
                    "commands": [{"action": "section_add", "local_id": uid()}]}
        page = base["document"]["pages"][0]["id"]
        def race(calls):
            barrier = Barrier(2, timeout=10)
            def run(pair):
                try:
                    barrier.wait()
                    return save_batch(pair[0], site.pk, pair[1])
                except Conflict:
                    return None
                finally:
                    connections.close_all()
            with ThreadPoolExecutor(2) as pool:
                return list(pool.map(run, calls))
        first = packet(base["id"])
        a, b = race([(users[0], first), (users[0], first)])
        self.assertEqual(a, b)
        self.assertIsNotNone(a)
        results = race([(actor, packet(a["revision"])) for actor in users])
        self.assertEqual(results.count(None), 1)
        self.assertEqual(save_batch(users[0], site.pk, first), a)
        self.assertEqual(CompositionRevision.objects.filter(site=site).count(), 3)
