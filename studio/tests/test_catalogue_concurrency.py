from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from django.contrib.auth.models import Group, User
from django.db import connections
from django.test import TransactionTestCase, skipUnlessDBFeature

from composition.models import CompositionRevision
from registre.models import Client, Site, SiteGrant
from registre.services import Conflict
from workspace.access import OPERATOR_GROUP


@skipUnlessDBFeature("has_select_for_update")
class AppearanceConcurrencyTests(TransactionTestCase):
    def test_theme_and_menu_compete_for_the_same_revision(self):
        from composition.appearance import modifier_apparence
        from composition.services import creer_brouillon, lire_revision, modifier_navigation

        customer = Client.objects.create(client_type="COMPANY", display_name="Site de recette")
        site = Site.objects.create(client=customer, name="Rivage")
        group = Group.objects.create(name=OPERATOR_GROUP)
        actors = []
        for username in ("graphisme", "navigation"):
            user = User.objects.create_user(username)
            user.groups.add(group)
            SiteGrant.objects.create(site=site, user=user, level="manage")
            actors.append(user)
        first = creer_brouillon(actors[0], site.pk, {"kind": "blank"})
        start = Barrier(2, timeout=10)

        def save(call, actor, command):
            try:
                start.wait()
                return call(actor, site.pk, first["id"], command)
            except Conflict:
                return None
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            theme = pool.submit(save, modifier_apparence, actors[0],
                                {"action": "theme", "values": {"gap": 23}})
            menu = pool.submit(save, modifier_navigation, actors[1],
                               {"action": "menu_add", "label": "Principal"})
            results = [task.result(timeout=20) for task in (theme, menu)]
        winners = [result for result in results if result]
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0]["parent_id"], first["id"])
        self.assertEqual(CompositionRevision.objects.filter(site=site).count(), 2)
        self.assertEqual(lire_revision(actors[0], site.pk, first["id"]), first)
