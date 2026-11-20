import asyncio
import json
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

from raccordement.transport import ProbeError, _probe, probe


class ContractTests(TestCase):
    def setUp(self):
        self.profile = SimpleNamespace(origin="https://site-a", site_id=uuid4(), instance_id=uuid4(),
                                       engine_version="1.0.0", image_digest="sha256:" + "a" * 64, marker="Atelier A")
        identity = {"site_id": str(self.profile.site_id), "instance_id": str(self.profile.instance_id)}
        self.version = dict(identity, contract_major=1, contract_minor=2, engine_version="1.0.0",
                            wagtail_version="7.4.4", image_digest=self.profile.image_digest)
        self.payload = {"identity": dict(identity, contract_major=1), "version": self.version,
                        "health": dict(identity, status="ready"), "render": "<main><p>Atelier A</p></main>"}

    def probe(self):
        async def read(url, tls, route, limit):
            if route == "render":
                return {"content-type": "text/html", "x-studio-site": str(self.profile.site_id),
                        "x-studio-instance": str(self.profile.instance_id)}, self.payload[route]
            return {"content-type": "application/json"}, json.dumps(self.payload[route])
        with patch("raccordement.transport._read", read):
            return asyncio.run(_probe(self.profile, None))

    def test_qualified_build_and_additive_minor(self):
        self.assertEqual(self.probe()["contract_minor"], 2)

    def test_other_instance_and_incompatible_version(self):
        self.payload["health"]["instance_id"] = str(uuid4())
        with self.assertRaisesRegex(ProbeError, "identity"):
            self.probe()
        self.version["contract_major"] = True
        with self.assertRaisesRegex(ProbeError, "incompatible"):
            self.probe()

    def test_marker_must_be_the_visible_reference(self):
        for html in ("<main><p>Atelier B</p></main>", "<main><p hidden>Atelier A</p></main>"):
            with self.subTest(html=html), self.assertRaisesRegex(ProbeError, "render"):
                self.payload["render"] = html
                self.probe()

    def test_connection_timeout_has_its_own_diagnostic(self):
        self.profile.ca = "/unused"
        self.profile.cert = "/unused"
        self.profile.key = "/unused"
        with patch("raccordement.transport.ssl.create_default_context"), patch(
            "raccordement.transport._read", side_effect=TimeoutError
        ), self.assertRaisesRegex(ProbeError, "timeout"):
            probe(self.profile)
