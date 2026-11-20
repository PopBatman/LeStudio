from datetime import datetime, timedelta, timezone as tz
from html.parser import HTMLParser
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from raccordement.models import SiteConnection
from registre.models import Client, ClientGrant, Site, SiteGrant
from workspace.access import OPERATOR_GROUP


class PageMarkup(HTMLParser):
    def __init__(self, response):
        super().__init__()
        self.links = []
        self.times = []
        self.feed(response.content.decode())

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
        if tag == "time":
            self.times.append(datetime.fromisoformat(attributes["datetime"]))


class SiteConnectionPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.operator = User.objects.create_user("operatrice-fictive")
        cls.operator.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        cls.owner = Client.objects.create(display_name="Maison Exemple", client_type="COMPANY")
        cls.site = Site.objects.create(name="Atelier fictif", client=cls.owner)
        cls.grant = SiteGrant.objects.create(site=cls.site, user=cls.operator, level="manage")

    def setUp(self):
        self.client.force_login(self.operator)
        self.url = f"/sites/{self.site.pk}/"
        self.confirmation = datetime(2025, 7, 11, 15, 24, 31, tzinfo=tz.utc)
        self.finish = self.confirmation + timedelta(days=1)

    def record(self, **fields):
        values = {
            "site": self.site, "attempt_id": uuid4(), "actor": self.operator,
            "confirmed_at": self.confirmation, "instance_id": uuid4(),
            "confirmed_profile": "atelier-fictif",
            "versions": {"wagtail_version": "7.3.2", "engine_version": "1.0.5",
                         "contract_major": 2, "contract_minor": 0},
            "started_at": self.finish - timedelta(seconds=2),
            "finished_at": self.finish, "expires_at": self.finish + timedelta(seconds=18),
            "diagnostic": "connected",
        }
        return SiteConnection.objects.create(**{**values, **fields})

    def assert_not_exposed(self, response, *markers):
        # Inspect template values as well as hidden and visible HTML.
        context_data = []
        for context in response.context:
            for value in context.flatten().values():
                if isinstance(value, (str, dict, list, tuple)):
                    context_data.append(str(value))
        for marker in markers:
            self.assertNotIn(marker, response.content.decode())
            self.assertNotIn(marker, "\n".join(context_data))

    def test_entry_resumes_current_revision_for_manager_and_reader(self):
        from composition.services import creer_brouillon
        entry = self.url + "atelier/"
        self.assertContains(self.client.get(self.url), "Créer le brouillon")
        creer_brouillon(self.operator, self.site.pk, {"kind": "blank"})
        self.assertContains(self.client.get(self.url), "Reprendre le brouillon")
        self.grant.level = "read"
        self.grant.save()
        response = self.client.get(self.url)
        self.assertContains(response, "Consulter le brouillon")
        self.assertContains(response, "Révision 1")
        self.assertIn(entry, PageMarkup(response).links)
        self.assertIn(entry + "canvas/", PageMarkup(response).links)

    def test_empty_site_without_domain(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Moteur Wagtail")
        self.assertContains(response, "Non raccordé")
        self.assertContains(response, "Aucune confirmation enregistrée")
        self.assertEqual(PageMarkup(response).times, [])
        self.assertFalse(SiteConnection.objects.filter(site=self.site).exists())

    def test_manager_sees_persisted_versions_identity_and_local_dates(self):
        row = self.record()
        self.site.domain = "boutique.exemple.test"
        self.site.save(update_fields=["domain"])
        response = self.client.get(self.url)
        for text in ("Raccordement confirmé", str(row.instance_id), row.confirmed_profile,
                     "7.3.2", "1.0.5", "2.0", "Dernière confirmation réussie", "Dernière tentative"):
            self.assertContains(response, text)
        markup = PageMarkup(response)
        self.assertCountEqual(markup.times, [self.confirmation, self.finish])
        self.assertContains(response, "Paris")
        self.assertRegex(response.content.decode(), r"17\s*(?:h\s*|:)24")
        self.assertFalse(any(self.site.domain in url or "/admin" in url for url in markup.links))
        self.assertNotContains(response, "En ligne")

    def test_reader_sees_last_failure_and_keeps_last_success(self):
        self.grant.level = "read"
        self.grant.save(update_fields=["level"])
        row = self.record(diagnostic="identity_mismatch")
        response = self.client.get(self.url)
        self.assertContains(response, "Dernière vérification en échec")
        self.assertContains(response, "7.3.2")
        self.assertCountEqual(PageMarkup(response).times, [self.confirmation, self.finish])
        self.assert_not_exposed(response, str(row.instance_id), row.confirmed_profile,
                                "identity_mismatch", "Modifier le site")

    def test_current_then_expired_attempt_uses_its_start(self):
        now = timezone.now()
        row = self.record(diagnostic="checking", started_at=now, finished_at=None,
                          expires_at=now + timedelta(hours=1))
        for offset, label in [(1, "Vérification en cours"), (-1, "Dernière vérification expirée")]:
            with self.subTest(label=label):
                row.expires_at = now + timedelta(hours=offset)
                row.save(update_fields=["expires_at"])
                response = self.client.get(self.url)
                self.assertContains(response, label)
                self.assertCountEqual(PageMarkup(response).times, [now, self.confirmation])

    def test_unknown_diagnostic_partial_versions_and_malformed_values(self):
        row = self.record(diagnostic="<bad-diagnostic>", confirmed_profile="/run/private.key",
                          versions={"wagtail_version": "7.3.2", "engine_version": "<private>",
                                    "unrelated": "private-extra-field"})
        response = self.client.get(self.url)
        self.assertContains(response, "Résultat indéterminé")
        self.assertContains(response, "7.3.2")
        self.assertContains(response, "Non renseign")
        self.assert_not_exposed(response, "bad-diagnostic", row.confirmed_profile,
                                "private-extra-field", "&lt;private&gt;", "<private>")

    def test_legacy_versions_cannot_override_confirmed_columns(self):
        row = self.record()
        other_instance = str(uuid4())
        for versions in (["unsupported"], {"profile": "wrong-profile", "instance_id": other_instance,
                                           "at": self.finish.isoformat()}):
            with self.subTest(kind=type(versions).__name__):
                row.versions = versions
                row.save(update_fields=["versions"])
                response = self.client.get(self.url)
                self.assertContains(response, row.confirmed_profile)
                self.assertContains(response, str(row.instance_id))
                self.assert_not_exposed(response, "wrong-profile", other_instance)
                self.assertCountEqual(PageMarkup(response).times, [self.confirmation, self.finish])

    def test_failure_before_first_success_and_incomplete_success(self):
        row = self.record(diagnostic="incompatible", confirmed_at=None, instance_id=None,
                          confirmed_profile="", versions={})
        for code, label in [("incompatible", "Dernière vérification en échec"),
                            ("connected", "Résultat indéterminé")]:
            with self.subTest(code=code):
                row.diagnostic = code
                row.save(update_fields=["diagnostic"])
                response = self.client.get(self.url)
                self.assertContains(response, label)
                self.assertContains(response, "Aucune confirmation enregistrée")
                self.assertEqual(PageMarkup(response).times, [self.finish])

    def test_cross_site_client_grant_and_revocation(self):
        self.record()
        other = Site.objects.create(name="Autre site fictif", client=self.owner)
        secret = self.record(site=other, confirmed_profile="autre-profil")
        ClientGrant.objects.create(client=self.owner, user=self.operator, level="manage")
        self.assert_not_exposed(self.client.get(self.url), secret.confirmed_profile, str(secret.instance_id))
        forbidden = self.client.get(f"/sites/{other.pk}/")
        self.assertEqual(forbidden.status_code, 404)
        self.assert_not_exposed(forbidden, secret.confirmed_profile, str(secret.instance_id))
        self.grant.delete()
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.operator.groups.clear()
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.client.logout()
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_consultation_is_read_only_for_all_requests(self):
        self.record()
        before = list(SiteConnection.objects.values())
        with patch("raccordement.services.probe") as probe, \
             patch("raccordement.services.load_profile") as profile, \
             CaptureQueriesContext(connection) as queries:
            self.assertContains(self.client.get(self.url), "Moteur Wagtail")
            self.assertEqual(self.client.head(self.url).status_code, 200)
            self.assertContains(self.client.get(self.url), "Moteur Wagtail")
            self.assertEqual(self.client.post(self.url).status_code, 405)
        self.assertFalse(any(q["sql"].lstrip().upper().startswith(("UPDATE", "INSERT", "DELETE"))
                             for q in queries.captured_queries))
        self.assertEqual(list(SiteConnection.objects.values()), before)
        probe.assert_not_called()
        profile.assert_not_called()
