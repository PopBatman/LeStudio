from datetime import timedelta
import secrets

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.utils import timezone

from workspace.access import OPERATOR_GROUP


class WorkspaceEntryTests(SimpleTestCase):
    def test_anonymous_visitor_reaches_login(self):
        response = self.client.get("/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url.split("?")[0], "/connexion/")
        self.assertIn("no-store", response.headers["Cache-Control"])

    @override_settings(STUDIO_UI_GALLERY=False)
    def test_login_styles_are_available_with_gallery_disabled(self):
        for url in ("/assets/gallery.css", "/assets/workspace.css", "/assets/fonts/dm-sans-latin.woff2"):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(any(response.streaming_content))
                response.close()
        self.assertEqual(self.client.get("/ui/").status_code, 404)
        self.assertEqual(self.client.get("/assets/gallery.js").status_code, 404)

    def test_existing_read_only_endpoints_keep_rejecting_writes(self):
        client = Client(enforce_csrf_checks=True)
        for url in ("/health/", "/ui/", "/ui/assets/gallery.css"):
            with self.subTest(url=url):
                self.assertEqual(client.post(url).status_code, 405)


class OperatorSessionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = secrets.token_urlsafe(32)
        cls.operator = get_user_model().objects.create_user("operatrice", password=cls.password)
        cls.group = Group.objects.create(name=OPERATOR_GROUP)
        cls.operator.groups.add(cls.group)

    def test_login_uses_workspace_and_logout_ends_access(self):
        client = Client(enforce_csrf_checks=True)
        credentials = {"username": self.operator.username, "password": self.password}
        self.assertEqual(client.post("/connexion/", credentials).status_code, 403)
        response = client.get("/connexion/")
        self.assertTemplateUsed(response, "workspace/login.html")
        credentials["csrfmiddlewaretoken"] = client.cookies[settings.CSRF_COOKIE_NAME].value
        response = client.post("/connexion/?next=https://other.invalid/", credentials)
        self.assertRedirects(response, "/", fetch_redirect_response=False)
        session_key = client.cookies[settings.SESSION_COOKIE_NAME].value
        self.assertTrue(client.cookies[settings.SESSION_COOKIE_NAME]["httponly"])
        self.assertEqual(client.cookies[settings.SESSION_COOKIE_NAME]["samesite"], "Lax")
        home = client.get("/")
        self.assertContains(home, self.operator.username)
        self.assertIn("no-store", home.headers["Cache-Control"])
        self.assertEqual(client.get("/deconnexion/").status_code, 405)
        self.assertEqual(client.post("/deconnexion/").status_code, 403)
        self.assertEqual(client.get("/").status_code, 200)
        response = client.post("/deconnexion/", {
            "csrfmiddlewaretoken": client.cookies[settings.CSRF_COOKIE_NAME].value,
        })
        self.assertRedirects(response, "/connexion/", fetch_redirect_response=False)
        self.assertFalse(Session.objects.filter(session_key=session_key).exists())
        self.assertEqual(client.get("/").status_code, 302)

    def test_login_refusals_share_one_error(self):
        User = get_user_model()
        inactive = User.objects.create_user("suspendu", password=self.password, is_active=False)
        inactive.groups.add(self.group)
        User.objects.create_superuser("admin", password=self.password)
        errors = []
        for username in ("inconnu", "suspendu", "admin", self.operator.username):
            with self.subTest(username=username):
                password = secrets.token_urlsafe(32) if username == self.operator.username else self.password
                response = self.client.post("/connexion/", {"username": username, "password": password})
                self.assertTemplateUsed(response, "workspace/login.html")
                self.assertEqual(response.status_code, 200)
                errors.append(list(response.context["form"].non_field_errors()))
                self.assertNotIn("_auth_user_id", self.client.session)
                self.assertFalse(password.encode() in response.content)
        self.assertTrue(errors[0])
        self.assertTrue(all(error == errors[0] for error in errors))

    def test_removing_membership_immediately_forbids_workspace(self):
        self.client.force_login(self.operator)
        self.operator.groups.remove(self.group)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "workspace/forbidden.html")
        self.assertIn("no-store", response.headers["Cache-Control"])
        self.assertRedirects(self.client.post("/deconnexion/"), "/connexion/", fetch_redirect_response=False)

    def test_expired_session_returns_to_login(self):
        self.client.force_login(self.operator)
        Session.objects.filter(session_key=self.client.session.session_key).update(
            expire_date=timezone.now() - timedelta(seconds=1),
        )
        response = self.client.get("/", follow=True)
        self.assertEqual(response.redirect_chain, [("/connexion/?next=/", 302)])
        self.assertTemplateUsed(response, "workspace/login.html")
