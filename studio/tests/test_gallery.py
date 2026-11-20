from django.test import SimpleTestCase, override_settings


class GalleryTests(SimpleTestCase):
    @override_settings(STUDIO_UI_GALLERY=False)
    def test_disabled_gallery_hides_page_and_assets(self):
        for path in ("/ui/", "/ui/assets/gallery.css", "/ui/assets/gallery.js"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path, HTTP_HOST="localhost").status_code, 404)

    @override_settings(STUDIO_UI_GALLERY=True)
    def test_enabled_gallery_renders_and_serves_compiled_assets(self):
        page = self.client.get("/ui/", HTTP_HOST="localhost")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "ui/gallery.html")
        self.assertNotContains(page, "<c-")
        for name, media in (("gallery.css", "text/css"), ("gallery.js", "javascript")):
            path = "/ui/assets/" + name
            with self.subTest(path=path):
                self.assertContains(page, path)
                response = self.client.get(path, HTTP_HOST="localhost")
                self.assertEqual(response.status_code, 200)
                self.assertIn(media, response["Content-Type"])
                self.assertTrue(b"".join(response.streaming_content).strip())

    @override_settings(STUDIO_UI_GALLERY=True)
    def test_gallery_is_read_only_and_exposes_only_its_assets(self):
        for path in ("/ui/", "/ui/assets/gallery.js"):
            with self.subTest(path=path):
                self.assertEqual(self.client.post(path, HTTP_HOST="localhost").status_code, 405)
        self.assertEqual(self.client.get("/ui/assets/requirements.txt", HTTP_HOST="localhost").status_code, 404)
