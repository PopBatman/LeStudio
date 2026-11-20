import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("workflow_cli_test", ROOT / "scripts/workflow.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name).resolve() / "studio"
        self.project.mkdir()
        self.task_dir = cli.new_task(self.project, "FEAT-001", "feature", "L’atelier dit \"oui\" : réglages")

    def tearDown(self):
        self.tmp.cleanup()

    def task(self):
        return json.loads((self.task_dir / "task.json").read_text())

    def save(self, task):
        (self.task_dir / "task.json").write_text(json.dumps(task, ensure_ascii=False))

    def fill(self, ui=False):
        for name in [*cli.BASE_DOCS, "REPORT.md", "REVIEW.md"] + (["VISUAL-REVIEW.md"] if ui else []):
            (self.task_dir / name).write_text("# " + name + "\n\nContrat explicite de la tâche.\n")
        task = self.task()
        task["scope"] = {"allowed_paths": ["src/**"], "forbidden_paths": ["src/private/**"]}
        task["authorization"] = {"reference": "user:conversation:scope-1", "actions": ["implement", "test", "review"]}
        task["ui_required"] = ui
        self.save(task)
        source = self.project / "src/example.py"
        source.parent.mkdir(exist_ok=True)
        source.write_text("def value():\n    return 1\n")

    def evidence(self, kind="test", outcome="passed", bind=True):
        path = self.task_dir / "evidence" / (kind + ".txt")
        path.write_text("Observation de vérification")
        item = {"kind": kind, "path": "evidence/" + path.name,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "observed_at": "2026-11-18T12:00:00+01:00", "revision": "test-revision", "outcome": outcome,
                "inputs": [{"path": "src/example.py", "sha256": hashlib.sha256((self.project / "src/example.py").read_bytes()).hexdigest()}] if bind else []}
        if bind:
            item["contract_sha256"] = cli.contract_fingerprint(self.project, "FEAT-001")
        task = self.task()
        task["evidence"].append(item)
        self.save(task)
        return item

    def test_new_has_no_implicit_mandate(self):
        task = self.task()
        self.assertEqual(task["state"], "DRAFT")
        self.assertIsNone(task["authorization"]["reference"])
        self.assertEqual(task["title"], "L’atelier dit \"oui\" : réglages")
        self.assertEqual(len(cli.status(self.project)), 1)

    def test_cli_creates_product_task_from_workflow_templates(self):
        tools = self.project.parent / "workflow-ai"
        script = tools / "scripts/workflow.py"
        script.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "scripts/workflow.py", script)
        shutil.copytree(ROOT / "templates", tools / "templates")
        subprocess.run([sys.executable, str(script), "new", "--id", "UI-002", "--kind", "component",
                        "--title", "Menu"], cwd=self.project, check=True, capture_output=True)
        spec = self.project / "work/items/UI-002/SPEC.md"
        expected = (tools / "templates/COMPONENT-SPEC.md").read_text().replace(cli.TODO, "")
        self.assertIn(expected, spec.read_text())
        self.assertFalse((tools / "work").exists())
        result = subprocess.run([sys.executable, str(script), "status"], cwd=tools, check=True, capture_output=True)
        self.assertEqual([task["id"] for task in json.loads(result.stdout)["tasks"]], ["FEAT-001", "UI-002"])

    def test_scaffold_cannot_pass_planning_until_completed(self):
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "planning")

    def test_planning_does_not_require_implementation_permission(self):
        for name in ("SPEC.md", "TASKLIST.md"):
            (self.task_dir / name).write_text("Document rédigé et examinable")
        result = cli.check_task(self.project, "FEAT-001", "planning")
        self.assertEqual(result["status"], "PASS")
        self.assertIsNone(self.task()["authorization"]["reference"])

    def test_ready_does_not_authorize_implementation(self):
        self.fill()
        task = self.task()
        task["state"] = "READY"
        task["authorization"] = {"reference": None, "actions": []}
        self.save(task)
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "implementation")

    def test_mandate_for_another_action_is_insufficient(self):
        self.fill()
        task = self.task()
        task["authorization"]["actions"] = ["plan"]
        self.save(task)
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "implementation")

    def test_empty_scope_is_rejected(self):
        self.fill()
        task = self.task()
        task["scope"]["allowed_paths"] = []
        self.save(task)
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "implementation")

    def test_check_never_changes_task_state(self):
        self.fill()
        before = (self.task_dir / "task.json").read_bytes()
        result = cli.check_task(self.project, "FEAT-001", "implementation")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual((self.task_dir / "task.json").read_bytes(), before)

    def test_verification_requires_passing_bound_evidence(self):
        self.fill()
        self.evidence(outcome="failed")
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "verification")
        task = self.task()
        task["evidence"] = []
        self.save(task)
        self.evidence()
        self.assertEqual(cli.check_task(self.project, "FEAT-001", "verification")["status"], "PASS")

    def test_changed_source_invalidates_evidence(self):
        self.fill()
        self.evidence()
        (self.project / "src/example.py").write_text("changed")
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "verification")

    def test_changed_contract_invalidates_evidence(self):
        self.fill()
        self.evidence()
        (self.task_dir / "SPEC.md").write_text("Autre comportement attendu")
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "verification")

    def test_tampered_evidence_fails(self):
        self.fill()
        self.evidence()
        (self.task_dir / "evidence/test.txt").write_text("Different report")
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "verification")

    def test_forbidden_paths_take_priority(self):
        self.fill()
        self.evidence()
        task = self.task()
        task["scope"]["forbidden_paths"] = ["src/example.py"]
        self.save(task)
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "verification")

    def test_private_source_is_refused_without_read(self):
        self.fill()
        item = self.evidence()
        task = self.task()
        task["scope"]["allowed_paths"] = ["**"]
        task["evidence"][0]["inputs"] = [{"path": ".env", "sha256": item["sha256"]}]
        self.save(task)
        with self.assertRaisesRegex(cli.WorkflowError, "hors périmètre"):
            cli.check_task(self.project, "FEAT-001", "verification")

    def test_ui_requires_mockup_then_screenshot(self):
        self.fill(ui=True)
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "implementation")
        self.evidence("mockup", "illustrative", bind=False)
        self.assertEqual(cli.check_task(self.project, "FEAT-001", "implementation")["status"], "PASS")
        self.evidence()
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "verification")
        self.evidence("screenshot")
        self.assertEqual(cli.check_task(self.project, "FEAT-001", "verification")["status"], "PASS")

    def test_release_requires_independent_review_and_scoped_mandate(self):
        self.fill()
        self.evidence()
        self.evidence("review")
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "release")
        task = self.task()
        task["review"] = {"reference": "reviewer:session-2", "independent": True}
        task["release_authorization"] = {"reference": "user:release-1", "actions": ["release"]}
        self.save(task)
        self.assertEqual(cli.check_task(self.project, "FEAT-001", "release")["status"], "PASS")

    def test_identifiers_and_kind_do_not_escape(self):
        for invalid in ("../outside", "FEAT-001/../other", "FEAT-../../x", "CONN-01"):
            with self.assertRaises(cli.WorkflowError):
                cli.new_task(self.project, invalid, "feature", "Titre")
        with self.assertRaises(cli.WorkflowError):
            cli.new_task(self.project, "CONN-002", "feature", "Titre")

    def test_existing_task_is_not_overwritten(self):
        before = (self.task_dir / "task.json").read_bytes()
        with self.assertRaises(cli.WorkflowError):
            cli.new_task(self.project, "FEAT-001", "feature", "New title")
        self.assertEqual((self.task_dir / "task.json").read_bytes(), before)

    def test_symlink_task_and_evidence_are_rejected(self):
        outside = self.project / "outside"
        outside.mkdir()
        (self.project / "work/items/FEAT-002").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(cli.WorkflowError):
            cli.load_task(self.project, "FEAT-002")
        self.fill()
        self.evidence()
        proof = self.task_dir / "evidence/test.txt"
        proof.unlink()
        proof.symlink_to(self.project / "src/example.py")
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "verification")

    def test_globs_are_component_wise_and_recursive(self):
        self.assertTrue(cli.path_matches("src/example.py", "src/**"))
        self.assertTrue(cli.path_matches("src/example.py", "src/**/*.py"))
        self.assertTrue(cli.path_matches("src/nested/example.py", "src/**/*.py"))
        self.assertFalse(cli.path_matches("src/nested/example.py", "src/*.py"))
        self.assertFalse(cli.path_matches("elsewhere/src/example.py", "src/**"))

    def test_malformed_types_fail_with_documentary_error(self):
        baseline = self.task()
        for key, value in (("kind", []), ("state", {}), ("schema_version", True)):
            with self.subTest(key=key):
                task = dict(baseline)
                task[key] = value
                self.save(task)
                with self.assertRaises(cli.WorkflowError):
                    cli.check_task(self.project, "FEAT-001", "planning")
        self.save(baseline)
        self.fill()
        self.evidence()
        baseline = self.task()
        for key in ("kind", "outcome"):
            with self.subTest(evidence_key=key):
                task = json.loads(json.dumps(baseline))
                task["evidence"][0][key] = []
                self.save(task)
                with self.assertRaises(cli.WorkflowError):
                    cli.check_task(self.project, "FEAT-001", "verification")

    def test_glob_depth_is_bounded(self):
        with self.assertRaises(cli.WorkflowError):
            cli.path_matches("/".join(["a"] * 101), "**")
        self.assertFalse(cli.path_matches("/".join(["a"] * 50), "/".join(["**"] * 50 + ["b"])))

    def test_active_pass_cannot_mask_failure_or_not_run(self):
        self.fill()
        self.evidence()
        for outcome in ("failed", "not_run"):
            with self.subTest(outcome=outcome):
                task = self.task()
                failure = dict(task["evidence"][0])
                failure["outcome"] = outcome
                failure["observed_at"] = "2026-11-18T13:00:00+01:00"
                task["evidence"] = [task["evidence"][0], failure]
                self.save(task)
                with self.assertRaises(cli.WorkflowError):
                    cli.check_task(self.project, "FEAT-001", "verification")

    def test_historical_red_and_current_green_keep_auditable_artifacts(self):
        self.fill()
        red = self.evidence(outcome="failed")
        old_artifact = self.task_dir / "evidence/test.txt"
        old_artifact.rename(self.task_dir / "evidence/red.txt")
        task = self.task()
        task["evidence"][0]["path"] = "evidence/red.txt"
        task["evidence"][0]["active"] = False
        self.save(task)
        (self.project / "src/example.py").write_text("def value():\n    return 2\n")
        self.evidence()
        self.assertEqual(cli.check_task(self.project, "FEAT-001", "verification")["status"], "PASS")
        self.assertEqual(len(self.task()["evidence"]), 2)
        (self.task_dir / "evidence/red.txt").write_text("Historical artifact changed")
        with self.assertRaises(cli.WorkflowError):
            cli.check_task(self.project, "FEAT-001", "verification")

    def test_active_is_a_boolean_and_historical_proof_cannot_pass_gate(self):
        self.fill()
        self.evidence()
        task = self.task()
        for value in ("false", 0, None, False):
            with self.subTest(value=value):
                task["evidence"][0]["active"] = value
                self.save(task)
                with self.assertRaises(cli.WorkflowError):
                    cli.check_task(self.project, "FEAT-001", "verification")

    def test_component_cannot_turn_off_visual_requirements(self):
        directory = cli.new_task(self.project, "UI-001", "component", "Bouton")
        task = json.loads((directory / "task.json").read_text())
        self.assertTrue(task["ui_required"])
        task["ui_required"] = False
        (directory / "task.json").write_text(json.dumps(task))
        with self.assertRaises(cli.WorkflowError):
            cli.load_task(self.project, "UI-001")


if __name__ == "__main__":
    unittest.main()
