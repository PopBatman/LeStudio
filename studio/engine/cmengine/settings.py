import os
import re
from uuid import UUID
from django.core.exceptions import ImproperlyConfigured

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
if len(SECRET_KEY) < 50:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY doit contenir au moins 50 caractères.")
STUDIO_SITE_ID = str(UUID(os.environ["STUDIO_SITE_ID"]))
ENGINE_INSTANCE_ID = str(UUID(os.environ["ENGINE_INSTANCE_ID"]))
ENGINE_IMAGE_DIGEST = os.environ["ENGINE_IMAGE_DIGEST"]
if not re.fullmatch(r"sha256:[0-9a-f]{64}", ENGINE_IMAGE_DIGEST):
    raise ImproperlyConfigured("Digest de lancement invalide.")
ENGINE_MARKER = os.environ["ENGINE_MARKER"]
if not ENGINE_MARKER.strip() or len(ENGINE_MARKER) > 200:
    raise ImproperlyConfigured("Marqueur de référence invalide.")
ALLOWED_HOSTS = os.environ.get("ENGINE_ALLOWED_HOSTS", "localhost").split(",")
DEBUG = False
ROOT_URLCONF = "cmengine.urls"
MIDDLEWARE = ["django.middleware.common.CommonMiddleware"]
INSTALLED_APPS = [
    "reference", "wagtail.sites", "wagtail.users", "wagtail.images",
    "wagtail.documents", "wagtail.search", "wagtail.admin", "wagtail",
    "modelcluster", "taggit", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
]
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True}]
DATABASES = {"default": {
    "ENGINE": "django.db.backends.postgresql", "HOST": os.environ["POSTGRES_HOST"],
    "NAME": os.environ["POSTGRES_DB"], "USER": os.environ["POSTGRES_USER"],
    "PASSWORD": os.environ["POSTGRES_PASSWORD"], "OPTIONS": {"connect_timeout": 2},
}}
MEDIA_ROOT = "/app/media"
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
WAGTAIL_SITE_NAME = "Moteur Studio"
WAGTAILADMIN_BASE_URL = "http://localhost"
WAGTAILSEARCH_BACKENDS = {"default": {"BACKEND": "wagtail.search.backends.database"}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True

# An unconfigured engine keeps its original diagnostic-only contract.
EDITORIAL_WAGTAIL_SITE_ID = int(os.environ.get("EDITORIAL_WAGTAIL_SITE_ID") or 0)

ENGINE_PREVIEW_ENABLED = os.environ.get("ENGINE_PREVIEW_ENABLED") == "1"
DATA_UPLOAD_MAX_MEMORY_SIZE = 4 * 1024 * 1024
