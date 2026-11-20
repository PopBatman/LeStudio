from hashlib import sha256
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.utils import timezone

from composition.preview import PreviewError, render_preview
from composition.services import creer_brouillon
from raccordement.models import SiteConnection
from raccordement.transport import canonical_json
from registre.models import Client, Site, SiteGrant
from workspace.access import OPERATOR_GROUP

from .test_composition_services import sample_document


class PreviewBridgeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice")
        self.user.groups.add(Group.objects.create(name=OPERATOR_GROUP))
        client = Client.objects.create(display_name="Atelier", client_type="COMPANY")
        self.site = Site.objects.create(client=client, name="Site exemple")
        self.grant = SiteGrant.objects.create(site=self.site, user=self.user, level="manage")
        self.doc = sample_document()
        self.revision = creer_brouillon(self.user, self.site.pk, {"kind": "blank"}, self.doc)
        self.page = self.doc["pages"][0]["id"]
        self.profile = SimpleNamespace(site_id=self.site.pk, instance_id=uuid4(), engine_version="1.0.0",
                                       image_digest="sha256:" + "1" * 64)
        now = timezone.now()
        self.link = SiteConnection.objects.create(
            site=self.site, confirmed_profile="a", confirmed_at=now, diagnostic="connected",
            instance_id=self.profile.instance_id, finished_at=now, started_at=now, expires_at=now,
            attempt_id=uuid4(), versions={"image_digest":self.profile.image_digest, "engine_version":"1.0.0"})
        self.grant.level = "read"
        self.grant.save()
        profile = patch("composition.preview.load_profile", return_value=self.profile)
        profile.start()
        self.addCleanup(profile.stop)
        network = patch("composition.preview.read_preview", side_effect=self.engine)
        self.network = network.start()
        self.addCleanup(network.stop)

    def engine(self, profile, payload):
        ids = [b["id"] for b in self.doc["pages"][0]["sections"][0]["blocks"]]
        html = '<main>' + ''.join(f'<p data-studio-block-id="{key}"></p>' for key in ids) + '</main>'
        for medium in payload["media"].values():
            html += f'<img src="data:image/png;base64,{medium["data"]}">'
        manifest = {k:payload[k] for k in ("site_id","instance_id","revision_id","revision_number","page_id",
                                           "definitions","articles","media")}
        manifest.update(sha256=sha256(canonical_json(payload)).hexdigest(), html_sha256=sha256(html.encode()).hexdigest(),
                        engine_version=profile.engine_version, image_digest=profile.image_digest,
                        wagtail_version="7.4.4", block_ids=ids, renderer_sha256="1"*64, css_sha256=sha256(b"").hexdigest(), fonts={})
        return {"html":html,"manifest":manifest}

    def render(self):
        return render_preview(self.user, self.site.pk, self.revision["id"], self.page)

    def test_read_only_grant_and_real_model_ids(self):
        self.assertEqual(self.render()["manifest"]["revision_id"], self.revision["id"])
        self.assertEqual(self.network.call_args.args[1]["document"]["pages"][1], {"id": self.doc["pages"][1]["id"]})
        self.grant.delete()
        with self.assertRaises(PreviewError):
            self.render()
        self.assertEqual(self.network.call_count, 1)

    def test_withdrawal_during_remote_read_hides_result(self):
        def withdrawn(profile, payload):
            self.grant.delete()
            return self.engine(profile, payload)
        self.network.side_effect = withdrawn
        with self.assertRaises(PreviewError):
            self.render()

    def test_manifest_must_agree_with_html_and_request(self):
        for change in ("identity","html","duplicate_dom","missing_dependency"):
            def changed(profile, payload):
                r = self.engine(profile, payload)
                if change == "identity":
                    r["manifest"]["site_id"] = str(uuid4())
                if change == "html":
                    r["html"] += "other"
                if change == "duplicate_dom":
                    r["html"] += r["html"]
                    r["manifest"]["html_sha256"] = sha256(r["html"].encode()).hexdigest()
                if change == "missing_dependency":
                    r["manifest"]["definitions"] = []
                return r
            self.network.side_effect = changed
            with self.subTest(change=change), self.assertRaises(PreviewError):
                self.render()

    def test_theme_media_and_revocation_are_site_scoped(self):
        from composition.catalogue import attribuer_media
        from composition.services import enregistrer_brouillon

        self.grant.level = "manage"
        self.grant.save()
        row = attribuer_media(self.site)
        self.doc.update(schema_version=4, theme={"media": {"kind": "media", "ref_id": str(row.pk)}})
        self.revision = enregistrer_brouillon(self.user, self.site.pk, self.revision["id"], self.doc)

        def disable(profile, payload):
            self.assertIn(str(row.pk), payload["media"])
            result = self.engine(profile, payload)
            result["manifest"]["media"] = {str(row.pk): payload["media"][str(row.pk)]["sha256"]}
            attribuer_media(self.site, actif=False)
            return result

        self.network.side_effect = disable
        with self.assertRaises(PreviewError) as refused:
            self.render()
        self.assertEqual(refused.exception.code, "inaccessible")
        with self.assertRaises(PreviewError):
            self.render()
        self.assertEqual(self.network.call_count, 1)
