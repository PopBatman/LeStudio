from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from wagtail.models import Page


class ReadContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_reference")

    def test_identity_version_and_availability(self):
        for path in ("identity", "version", "health"):
            response = self.client.get(f"/internal/{path}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["site_id"], settings.STUDIO_SITE_ID)
            self.assertEqual(response.json()["instance_id"], settings.ENGINE_INSTANCE_ID)
            self.assertEqual(self.client.post(f"/internal/{path}").status_code, 405)
        self.assertEqual(self.client.get("/internal/health").json()["status"], "ready")
        self.assertEqual(self.client.get("/internal/version").json()["image_digest"], settings.ENGINE_IMAGE_DIGEST)

    def test_render_uses_live_revision_and_does_not_publish_drafts(self):
        page = Page.objects.get(slug="reference-studio").specific
        page.marker = "Autre brouillon"
        page.save_revision()
        render = self.client.get("/internal/render")
        self.assertContains(render, settings.ENGINE_MARKER)
        self.assertNotContains(render, "Autre brouillon")
        self.assertEqual(render.headers["X-Studio-Instance"], settings.ENGINE_INSTANCE_ID)
        self.assertEqual(self.client.post("/internal/render").status_code, 405)
        page.unpublish()
        self.assertEqual(self.client.get("/internal/health").status_code, 503)
        self.assertEqual(self.client.get("/internal/render").status_code, 503)

    def test_repeated_initialization_keeps_published_revision(self):
        page = Page.objects.get(slug="reference-studio")
        call_command("seed_reference")
        self.assertEqual(Page.objects.get(slug="reference-studio").live_revision_id, page.live_revision_id)


class EditorialTests(TestCase):
    def test_published_token_excludes_draft_restricted_foreign_and_ambiguous(self):
        from .models import ArticlePage
        from wagtail.models import PageViewRestriction, Site

        site = Site.objects.get(is_default_site=True)
        root = site.root_page
        article = root.add_child(instance=ArticlePage(title="Article fictif", slug="article"))
        path = f"/internal/editorial/v1/article/{article.pk}"
        rev = article.save_revision()
        with self.settings(EDITORIAL_WAGTAIL_SITE_ID=site.pk):
            self.assertEqual(self.client.get(path).status_code, 404)
            rev.publish()
            article.refresh_from_db()
            article.title = "Brouillon privé"
            article.save_revision()
            self.assertEqual(self.client.get(path).json(), dict(site_id=settings.STUDIO_SITE_ID,
                instance_id=settings.ENGINE_INSTANCE_ID, type="article", page_id=article.pk,
                published_revision_id=str(rev.pk)))
            foreign = Site.objects.create(hostname="voisin", root_page=article)
            self.assertEqual(self.client.get(path).status_code, 404)
            foreign.root_page = root
            foreign.save()
            self.assertEqual(self.client.get(path).status_code, 404)
            foreign.delete()
            PageViewRestriction.objects.create(page=root, restriction_type="login")
            self.assertEqual(self.client.get(path).status_code, 404)

    def test_native_admin_publishes_article_and_enforces_page_permissions(self):
        import json
        from django.contrib.auth.models import Permission, User
        from django.test import Client
        from reference.models import ArticlePage
        from wagtail.models import Site

        call_command("seed_reference")
        root = Site.objects.get(is_default_site=True).root_page
        User.objects.create_superuser("admin", password="mot-de-passe-test")
        limited = User.objects.create_user("limited", password="mot-de-passe-test")
        limited.user_permissions.add(Permission.objects.get(
            content_type__app_label="wagtailadmin", codename="access_admin"))
        from unittest.mock import patch
        with patch.dict("os.environ", {"ENGINE_ADMIN_ORIGIN": "http://localhost"}):
            from cmengine import admin_settings
        with self.settings(ROOT_URLCONF=admin_settings.ROOT_URLCONF, MIDDLEWARE=admin_settings.MIDDLEWARE,
                           TEMPLATES=admin_settings.TEMPLATES):
            def session(username):
                client = Client(enforce_csrf_checks=True)
                client.get("/admin/login/")
                result = client.post("/admin/login/", {"username": username, "password": "mot-de-passe-test",
                                     "csrfmiddlewaretoken": client.cookies["csrftoken"].value})
                self.assertEqual(result.status_code, 302)
                return client

            admin = session("admin")
            rich_text = {"blocks": [{"key": "abcde", "type": "unstyled", "text": "Corps éditorial",
                                     "depth": 0, "inlineStyleRanges": [], "entityRanges": [], "data": {}}],
                         "entityMap": {}}
            form = {"csrfmiddlewaretoken": admin.cookies["csrftoken"].value,
                    "slug": "article", "title": "Article fictif", "body": json.dumps(rich_text),
                    "action-publish": "action-publish"}
            response = admin.post(f"/admin/pages/add/reference/articlepage/{root.pk}/", form)
            self.assertEqual(response.status_code, 302)
            article = ArticlePage.objects.get(slug="article")
            self.assertTrue(article.live_revision_id)
            self.assertContains(admin.get("/pages/article/", HTTP_HOST="localhost"), "Corps éditorial")
            editor = session("limited")
            form.update(title="Modification refusée", csrfmiddlewaretoken=editor.cookies["csrftoken"].value)
            edit = f"/admin/pages/{article.pk}/edit/"
            self.assertIn(editor.get(edit).status_code, (302, 403))
            self.assertIn(editor.post(edit, form).status_code, (302, 403))
            article.refresh_from_db()
            self.assertEqual(article.title, "Article fictif")
