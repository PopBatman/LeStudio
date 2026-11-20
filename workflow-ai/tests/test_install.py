import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("workflow_installer_test", ROOT / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name).resolve()
        self.source = self.base / "package"
        self.product = self.base / "studio"
        self.target = self.base / "projet-équipe"
        self.source.mkdir()
        for name, data in {"README.md": b"Workflow", "AGENTS.md": b"Rules", "CLAUDE.md": b"Router", "docs/example.md": b"Document"}.items():
            path = self.source / name
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_bytes(data)
        self.product.mkdir()
        (self.product / "README.md").write_bytes(b"Projet Django/Wagtail")
        self.refresh_manifest()

    def tearDown(self):
        self.tmp.cleanup()

    def refresh_manifest(self):
        self.manifest = {"schema_version": 2, "package": "workflow-ai-studio", "version": "1.0.0", "files": [], "project_files": []}
        for key, root in (("files", self.source), ("project_files", self.product)):
            for path in sorted(root.rglob("*")):
                if not path.is_file() or path.name == "MANIFEST.json":
                    continue
                data = path.read_bytes()
                self.manifest[key].append({"path": path.relative_to(root).as_posix(),
                                           "size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        self.write_manifest()

    def write_manifest(self):
        (self.source / "MANIFEST.json").write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_dry_run_is_read_only(self):
        result = installer.install(self.source, self.target)
        self.assertEqual(result["mode"], "dry-run")
        self.assertFalse(self.target.exists())

    def test_fresh_install_and_idempotence(self):
        result = installer.install(self.source, self.target, apply=True)
        self.assertGreater(result["writes"], 0)
        self.assertEqual((self.target / "workflow-ai/docs/example.md").read_bytes(), b"Document")
        self.assertEqual((self.target / "studio/README.md").read_bytes(), b"Projet Django/Wagtail")
        self.assertFalse((self.target / "studio/workflow-ai").exists())
        self.assertFalse((self.target / "studio/AGENTS.md").exists())
        self.assertIn(b"workflow-ai/AGENTS.md", (self.target / "AGENTS.md").read_bytes())
        self.assertEqual(installer.install(self.source, self.target, apply=True)["writes"], 0)

    def test_legacy_install_keeps_original_layout_and_bridge(self):
        self.manifest["schema_version"] = 1
        del self.manifest["project_files"]
        self.write_manifest()
        installer.install(self.source, self.target, apply=True)
        self.assertEqual((self.target / "AGENTS.md").read_bytes(), installer.LEGACY_BLOCK)
        self.assertFalse((self.target / "studio").exists())
        self.assertEqual(installer.install(self.source, self.target, apply=True)["writes"], 0)

    def test_product_conflict_blocks_all_writes(self):
        doc = self.target / "studio/README.md"
        doc.parent.mkdir(parents=True)
        doc.write_bytes(b"Projet existant")
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.target, apply=True)
        self.assertEqual(doc.read_bytes(), b"Projet existant")
        self.assertFalse((self.target / "workflow-ai").exists())

    def test_changed_product_source_is_rejected_before_writing(self):
        (self.product / "README.md").write_bytes(b"Unexpected content")
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.target, apply=True)
        self.assertFalse(self.target.exists())

    def test_cannot_install_inside_another_installed_product(self):
        installer.install(self.source, self.target, apply=True)
        for path in (self.target / "studio", self.target / "studio/nested"):
            with self.subTest(path=path), self.assertRaises(installer.InstallError):
                installer.install(self.source, path, apply=True)
            self.assertFalse((path / "workflow-ai").exists())

    def test_existing_instructions_are_preserved_exactly(self):
        self.target.mkdir()
        before = "# Instructions de l’équipe\n\nConserver cette phrase.\n".encode()
        (self.target / "AGENTS.md").write_bytes(before)
        installer.install(self.source, self.target, apply=True)
        after = (self.target / "AGENTS.md").read_bytes()
        self.assertTrue(after.startswith(before))
        self.assertEqual(after.count(installer.START), 1)
        self.assertEqual(installer.install(self.source, self.target, apply=True)["writes"], 0)

    def test_conflict_has_no_partial_writes(self):
        conflict = self.target / "workflow-ai/docs/example.md"
        conflict.parent.mkdir(parents=True)
        conflict.write_bytes(b"Locally modified")
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.target, apply=True)
        self.assertEqual(conflict.read_bytes(), b"Locally modified")
        self.assertFalse((self.target / "workflow-ai/README.md").exists())
        self.assertFalse((self.target / "AGENTS.md").exists())

    def test_existing_runtime_files_are_left_untouched(self):
        installer.install(self.source, self.target, apply=True)
        extra = self.target / "workflow-ai/work/new-note.md"
        extra.parent.mkdir()
        extra.write_text("My work")
        installer.install(self.source, self.target, apply=True)
        self.assertEqual(extra.read_text(), "My work")

    def test_tampered_source_is_rejected_before_writing(self):
        (self.source / "README.md").write_text("Tampered")
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.target, apply=True)
        self.assertFalse(self.target.exists())

    def test_target_inside_package_is_rejected(self):
        for folder in (self.source, self.product):
            for target in (folder, folder / "nested"):
                with self.subTest(target=target), self.assertRaises(installer.InstallError):
                    installer.install(self.source, target, apply=True)
            self.assertFalse((folder / "workflow-ai").exists())

    def test_target_symlink_and_symlink_parent_are_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.target.symlink_to(outside, target_is_directory=True)
        for target in (self.target, self.target / "child"):
            with self.assertRaises(installer.InstallError):
                installer.install(self.source, target, apply=True)
        self.assertEqual(list(outside.iterdir()), [])

    def test_destination_file_symlink_is_rejected(self):
        self.target.mkdir()
        secret = self.base / "elsewhere"
        secret.write_text("unchanged")
        (self.target / "AGENTS.md").symlink_to(secret)
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.target, apply=True)
        self.assertEqual(secret.read_text(), "unchanged")

    def test_manifest_traversal_is_rejected(self):
        self.manifest["files"][0]["path"] = "../elsewhere"
        self.write_manifest()
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.target, apply=True)
        self.assertFalse(self.target.exists())

    def test_manifest_secret_path_is_rejected(self):
        self.manifest["files"][0]["path"] = ".env"
        self.write_manifest()
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.target, apply=True)

    def test_source_symlink_is_rejected(self):
        path = self.source / "docs/example.md"
        path.unlink()
        elsewhere = self.base / "source-copy"
        elsewhere.write_bytes(b"Document")
        path.symlink_to(elsewhere)
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.target, apply=True)

    def test_modified_managed_block_is_rejected(self):
        self.target.mkdir()
        (self.target / "AGENTS.md").write_bytes(installer.BLOCK.replace(b"workflow-ai/README.md", b"other/README.md"))
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.target, apply=True)
        self.assertFalse((self.target / "workflow-ai").exists())

    def test_write_failure_does_not_publish_partial_file(self):
        with patch.object(installer.os, "fsync", side_effect=OSError("simulated disk error")):
            with self.assertRaises(OSError):
                installer.install(self.source, self.target, apply=True)
        self.assertFalse(self.target.exists())
        self.assertGreater(installer.install(self.source, self.target, apply=True)["writes"], 0)


if __name__ == "__main__":
    unittest.main()
