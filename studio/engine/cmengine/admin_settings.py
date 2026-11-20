"""Separate browser process for native Wagtail sessions and page permissions."""
from .settings import *  # noqa: F403

ROOT_URLCONF = "cmengine.admin_urls"
WAGTAILADMIN_BASE_URL = os.environ["ENGINE_ADMIN_ORIGIN"]
SESSION_COOKIE_NAME = "studio_engine_" + ENGINE_INSTANCE_ID.replace("-", "") + "_session"
CSRF_COOKIE_NAME = "studio_engine_" + ENGINE_INSTANCE_ID.replace("-", "") + "_csrf"
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = WAGTAILADMIN_BASE_URL.startswith("https://")
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
TEMPLATES = [{**TEMPLATES[0], "OPTIONS": {"context_processors": [
    "django.template.context_processors.request", "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
]}}]
