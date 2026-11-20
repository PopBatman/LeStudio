from concurrent.futures import ThreadPoolExecutor
from functools import partial
from threading import Barrier

from django.contrib.auth.models import Group, User
from django.db import connections
from django.test import TransactionTestCase, skipUnlessDBFeature

from composition.appearance import modifier_apparence
from composition.catalogue import installer_version
from composition.editor import creer_atelier, modifier_structure
from composition.models import CompositionRevision
from composition.services import creer_brouillon, lire_brouillon, lire_revision
from registre.models import Client, Site, SiteGrant
from registre.services import Conflict
from workspace.access import OPERATOR_GROUP


@skipUnlessDBFeature("has_select_for_update")
class EditorConcurrencyTests(TransactionTestCase):
    def setUp(self):
        client = Client.objects.create(client_type="COMPANY", display_name="Client de recette")
        self.site = Site.objects.create(client=client, name="Atelier")
        group = Group.objects.create(name=OPERATOR_GROUP)
        self.editor = User.objects.create_user("atelier")
        self.colleague = User.objects.create_user("collegue")
        for actor in (self.editor, self.colleague):
            actor.groups.add(group)
            SiteGrant.objects.create(site=self.site, user=actor, level="manage")

    def race(self, calls):
        start = Barrier(2, timeout=10)

        def run(call):
            try:
                start.wait()
                return call()
            except Conflict:
                return None
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            tasks = [pool.submit(run, call) for call in calls]
            winners = [result for task in tasks if (result := task.result(timeout=20)) is not None]
        self.assertEqual(len(winners), 1)
        return winners[0]

    def test_pages_and_editor_compete_to_create_the_draft(self):
        winner = self.race([
            partial(creer_brouillon, self.colleague, self.site.pk, {"kind": "blank"}),
            partial(creer_atelier, self.editor, self.site.pk, "blank"),
        ])
        self.assertEqual(winner, lire_brouillon(self.editor, self.site.pk))
        self.assertIsNone(winner["parent_id"])
        self.assertEqual(CompositionRevision.objects.filter(site=self.site).count(), 1)

    def test_appearance_and_editor_compete_to_save_the_same_base(self):
        draft = creer_atelier(self.editor, self.site.pk, "blank")
        page = draft["document"]["pages"][0]["id"]

        def edit():
            revision, _ = modifier_structure(self.editor, self.site.pk, draft["id"],
                                              {"action": "section_add", "page": page})
            return revision

        winner = self.race([
            partial(modifier_apparence, self.colleague, self.site.pk, draft["id"],
                    {"action": "theme", "values": {"gap": 27}}),
            edit,
        ])
        self.assertEqual(winner["parent_id"], draft["id"])
        self.assertEqual(winner, lire_brouillon(self.colleague, self.site.pk))
        self.assertEqual(lire_revision(self.editor, self.site.pk, draft["id"]), draft)
        self.assertEqual(CompositionRevision.objects.filter(site=self.site).count(), 2)

    def test_canvas_and_structured_editor_share_the_revision_lock(self):
        installer_version(None, "heading", 1, "Titre", "heading")
        installer_version(None, "text", 1, "Texte", "text")
        draft = creer_atelier(self.editor, self.site.pk, "template")
        page = draft["document"]["pages"][0]
        block = page["sections"][0]["blocks"][1]
        target = {"page": page["id"], "id": block["id"]}

        def save(actor, **command):
            revision, _ = modifier_structure(actor, self.site.pk, draft["id"], {**target, **command})
            return revision

        winner = self.race([
            partial(save, self.editor, action="block_place", format="mobile", patch={"width": 75}),
            partial(save, self.colleague, action="block_edit", definition=block["definition"],
                    props={"text": "Texte révisé"}),
        ])
        self.assertEqual(winner["parent_id"], draft["id"])
        self.assertEqual(winner, lire_brouillon(self.editor, self.site.pk))
        self.assertEqual(draft, lire_revision(self.editor, self.site.pk, draft["id"]))
        self.assertEqual(CompositionRevision.objects.filter(site=self.site).count(), 2)
