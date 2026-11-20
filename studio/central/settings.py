import os
from pathlib import Path
from urllib.parse import urlsplit

from .portal import portal_origin

from django.core.exceptions import ImproperlyConfigured


def required_setting(name, *, min_length=1, default=""):
    value = os.environ.get(name, default)
    if len(value.strip()) < min_length:
        raise ImproperlyConfigured(f"{name} doit contenir au moins {min_length} caractère(s).")
    return value


BASE_DIR = Path(__file__).resolve().parent.parent
STUDIO_EDITOR_MODE = os.environ.get("STUDIO_EDITOR_MODE", "coexistence")
if STUDIO_EDITOR_MODE not in ("coexistence", "builder", "compatibility"):
    raise ImproperlyConfigured("STUDIO_EDITOR_MODE doit être coexistence, builder ou compatibility.")
STUDIO_UI_GALLERY = os.environ.get("STUDIO_UI_GALLERY") == "1"
SECRET_KEY = required_setting("DJANGO_SECRET_KEY", min_length=50)
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
STUDIO_PORTAL_ORIGIN = portal_origin(os.environ.get("STUDIO_PORTAL_ORIGIN", "http://127.0.0.1:8000"))
STUDIO_PORTAL_CONTACT = os.environ.get("STUDIO_PORTAL_CONTACT", "").strip()
portal_host = urlsplit(STUDIO_PORTAL_ORIGIN).hostname
STUDIO_PORTAL_PUBLIC_HOST = None if portal_host in ALLOWED_HOSTS else portal_host
if STUDIO_PORTAL_PUBLIC_HOST:
    ALLOWED_HOSTS.append(STUDIO_PORTAL_PUBLIC_HOST)
CSRF_TRUSTED_ORIGINS = [STUDIO_PORTAL_ORIGIN]

ROOT_URLCONF = "central.urls"
LANGUAGE_CODE = "fr"
LOGIN_URL = "login"
MIDDLEWARE = [
    "central.portal.PortalHostMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django_cotton",
    "workspace",
    "registre",
    "raccordement",
    "composition",
    "depots",
]
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"django.contrib.auth.password_validation.{name}"}
    for name in (
        "UserAttributeSimilarityValidator",
        "MinimumLengthValidator",
        "CommonPasswordValidator",
        "NumericPasswordValidator",
    )
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "composition.editor_navigation.navigation_context",
                "django.contrib.auth.context_processors.auth",
            ],
        },
    }
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": required_setting("STUDIO_DB_HOST", default="db"),
        "PORT": 5432,
        "NAME": "studio_db",
        "USER": "studio_app",
        "PASSWORD": required_setting("STUDIO_DB_PASSWORD"),
        "OPTIONS": {"connect_timeout": 3},
    }
}
