import os
from pathlib import Path
import secrets
import subprocess
import sys
import unittest


class ConfigurationTests(unittest.TestCase):
    def test_invalid_settings_refused_without_disclosing_values(self):
        for key, value in (
            ("DJANGO_SECRET_KEY", None),
            ("DJANGO_SECRET_KEY", "short-test-value"),
            ("STUDIO_DB_PASSWORD", None),
            ("STUDIO_DB_PASSWORD", "   "),
            ("STUDIO_DB_HOST", ""),
        ):
            with self.subTest(key=key, missing=value is None):
                env = dict(os.environ, DJANGO_SECRET_KEY=secrets.token_hex(32),
                           STUDIO_DB_PASSWORD=secrets.token_hex(32), STUDIO_DB_HOST="db")
                if value is None:
                    del env[key]
                else:
                    env[key] = value
                proc = subprocess.run(
                    [sys.executable, "manage.py", "check"],
                    cwd=Path(__file__).resolve().parents[1],
                    env=env, capture_output=True, text=True, timeout=15,
                )
                self.assertNotEqual(proc.returncode, 0)
                self.assertIn(key, proc.stderr)
                for name in ("DJANGO_SECRET_KEY", "STUDIO_DB_PASSWORD"):
                    secret = env.get(name)
                    if secret and secret.strip():
                        self.assertNotIn(secret, proc.stdout + proc.stderr)
