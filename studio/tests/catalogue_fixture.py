from django.test import TestCase

from composition.catalogue import installer_version
from composition.catalogue_v1 import TITLES


class CatalogueTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # TransactionTestCase flushes migration data in a reused PostgreSQL test database.
        for key, title in {**TITLES, "article": "Article Wagtail"}.items():
            installer_version(None, key, 1, title, key)
