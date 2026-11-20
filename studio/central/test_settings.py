"""Run the unit suite in an isolated database with the application's normal settings."""
from .settings import *  # noqa: F403

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
