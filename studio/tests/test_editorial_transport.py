import asyncio
import json
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import TestCase as DatabaseTestCase
from registre.models import Client, Site, SiteGrant
from raccordement.services import editorial_admin_url, verify_link
from workspace.access import OPERATOR_GROUP
from raccordement import transport


class PublishedReadTests(TestCase):
    def test_only_accepts_exact_identity_type_page_and_published_token(self):
        profile = SimpleNamespace(origin="https://api-a:8443", site_id="a", instance_id="b")
        body = dict(site_id="a", instance_id="b", type="article", page_id=42, published_revision_id="7")
        for changes in ({}, {"site_id":"b"}, {"page_id":True}, {"type":"reference"},
                        {"published_revision_id":"0"}, {"title":"privé"}):
            with self.subTest(changes=changes), patch.object(transport, "_read", new_callable=AsyncMock) as read:
                read.return_value = ({"content-type":"application/json"}, json.dumps({**body, **changes}))
                result = transport._published(profile, None, 42)
                if changes:
                    with self.assertRaises(transport.ProbeError):
                        asyncio.run(result)
                else:
                    self.assertEqual(asyncio.run(result), "7")
                    self.assertEqual(read.await_args.args[2:], ("editorial/v1/article/42", 16384))

    def test_timeout_and_invalid_input_do_not_expose_internal_cause(self):
        from raccordement.transport import ProbeError, read_published_article
        with patch.object(transport, "_run", side_effect=ProbeError("timeout")) as run:
            for page in (0, True, "https://elsewhere", 2147483648):
                with self.assertRaisesRegex(ProbeError, "inaccessible"):
                    read_published_article(None, page)
            run.assert_not_called()
            with self.assertRaisesRegex(ProbeError, "indisponible"):
                read_published_article(None, 42)

    def test_browser_admin_destinations(self):
        from raccordement.profiles import valid_admin_url
        for url in ("http://127.0.0.1:8011/admin/", "http://[::1]/admin/", "https://atelier.test/admin/"):
            self.assertTrue(valid_admin_url(url), url)
        for url in ("http://atelier.test/admin/", "https://user@atelier.test/admin/",
                    "https://atelier.test/admin/?suite=url", "//atelier.test/admin/",
                    "https://atelier.test/admin/\n", "https://atelier.test/internal/"):
            self.assertFalse(valid_admin_url(url), url)


class EditorialAdminLinkTests(DatabaseTestCase):
    def test_link_requires_manager_and_current_confirmed_instance(self):
        user = User.objects.create_user("operateur")
        user.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        client = Client.objects.create(display_name="Atelier", client_type="COMPANY")
        site = Site.objects.create(client=client, name="Site fictif")
        grant = SiteGrant.objects.create(site=site, user=user, level="manage")
        profile = SimpleNamespace(site_id=site.pk, instance_id=uuid4(), alias="test",
                                  engine_version="1.0.0", image_digest="sha256:"+"a"*64,
                                  admin_url="http://127.0.0.1:18571/admin/")
        versions = {"engine_version": profile.engine_version, "image_digest": profile.image_digest}
        with patch("raccordement.services.load_profile", return_value=profile), patch(
                "raccordement.services.probe", return_value=versions):
            self.assertEqual(editorial_admin_url(user, site), "")
            verify_link(user, site.pk, profile.alias)
            self.assertEqual(editorial_admin_url(user, site), profile.admin_url)
            grant.level = "read"
            grant.save()
            self.assertEqual(editorial_admin_url(user, site), "")
            grant.level = "manage"
            grant.save()
            profile.instance_id = uuid4()
            self.assertEqual(editorial_admin_url(user, site), "")
