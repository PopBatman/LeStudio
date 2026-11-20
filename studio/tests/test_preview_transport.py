import asyncio
from hashlib import sha256
import json
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from raccordement.transport import ProbeError, _preview, canonical_json


class PreviewTransportTests(TestCase):
    def setUp(self):
        self.profile = SimpleNamespace(site_id=uuid4(), instance_id=uuid4(), origin="https://site.test",
            image_digest="sha256:" + "a" * 64, engine_version="1")
        self.identity = {"site_id": str(self.profile.site_id), "instance_id": str(self.profile.instance_id),
                         "contract_major": 1}
        self.version = {**self.identity, "capabilities": ["preview.v1"], "contract_minor": 0,
                        "engine_version": "1", "image_digest": self.profile.image_digest, "wagtail_version": "7.4.4"}

    def replies(self, *items):
        return [({"content-type": "application/json"}, json.dumps(item)) for item in items]

    def test_authenticates_identity_version_and_capability_before_sending_draft(self):
        for changes in ({"site_id": str(uuid4())}, {"image_digest": "changed"}, {"capabilities": []}):
            with self.subTest(changes=changes), patch("raccordement.transport._read", new_callable=AsyncMock) as read:
                read.side_effect = self.replies(self.identity, {**self.version, **changes})
                with self.assertRaises(ProbeError):
                    asyncio.run(_preview(self.profile, None, {"title": "Privé"}))
                self.assertEqual([c.args[2] for c in read.await_args_list], ["identity", "version"])

    def test_request_binds_all_inputs_and_result_version(self):
        payload = {"title": "Privé"}
        with patch("raccordement.transport._read", new_callable=AsyncMock) as read:
            for version in ("7.4.4", "other"):
                read.side_effect = self.replies(self.identity, self.version, {"manifest": {"wagtail_version": version}})
                if version == "other":
                    with self.assertRaises(ProbeError):
                        asyncio.run(_preview(self.profile, None, payload))
                else:
                    asyncio.run(_preview(self.profile, None, payload))
                route, bound, body = read.await_args.args[2:]
                self.assertEqual(route, "preview/v1/render")
                self.assertEqual(bound, 8 * 1024 * 1024)
                self.assertEqual(json.loads(body), {"payload": payload, "sha256": sha256(canonical_json(payload)).hexdigest()})
