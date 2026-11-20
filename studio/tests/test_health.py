from unittest.mock import patch

from django.db import OperationalError
from django.test import SimpleTestCase


class HealthTests(SimpleTestCase):
    @patch("central.urls.connection")
    def test_database_failure_returns_only_status(self, database):
        database.cursor.side_effect = OperationalError("internal database detail")
        response = self.client.get("/health/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "unavailable"})
        self.assertIn("no-store", response.headers["Cache-Control"])

    def test_unrecognized_host_is_rejected_before_database_access(self):
        response = self.client.get("/health/", HTTP_HOST="outside.invalid")
        self.assertEqual(response.status_code, 400)

    def test_write_method_is_rejected_before_database_access(self):
        response = self.client.post("/health/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 405)
