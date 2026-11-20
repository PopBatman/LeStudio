from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase, override_settings

from central.portal import portal_origin


class PortalHostTests(SimpleTestCase):
    def test_share_origin_is_explicit(self):
        self.assertEqual(portal_origin("https://DEPOTS.example.test/"), "https://depots.example.test")
        self.assertEqual(portal_origin("http://localhost:8020"), "http://localhost:8020")
        for value in ("", "http://depots.example.test", "https://depots.example.test/site"):
            with self.subTest(value=value), self.assertRaises(ImproperlyConfigured):
                portal_origin(value)

    @override_settings(ALLOWED_HOSTS=["depot.example.test", "localhost"],
                       STUDIO_PORTAL_PUBLIC_HOST="depot.example.test")
    def test_external_portal_and_private_console_have_separate_entry_points(self):
        for host in ("depot.example.test", "DEPOT.example.test."):
            self.assertEqual(self.client.get("/connexion/", HTTP_HOST=host).status_code, 404)
            self.assertEqual(self.client.get("/assets/depot-public.css", HTTP_HOST=host).status_code, 200)
        self.assertEqual(self.client.get("/connexion/", HTTP_HOST="localhost").status_code, 200)
