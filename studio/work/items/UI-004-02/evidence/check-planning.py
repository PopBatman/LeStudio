#!/usr/bin/env python3
"""Contrôle documentaire complémentaire du seul lot Architecture UI-004-02."""
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[5]
ID = "UI-004-02"
spec = importlib.util.spec_from_file_location("workflow_t02", ROOT / "workflow-ai/scripts/workflow.py")
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)
# Identité Notion préexistante ; aucune modification du workflow partagé.
workflow.TASK_ID = re.compile(r"^UI-004-02$")
workflow.PREFIX["architecture"] = "UI"

def main():
    assert workflow.TASK_ID.fullmatch(ID)
    assert not workflow.TASK_ID.fullmatch("../UI-004-02")
    directory, task = workflow.load_task(ROOT / "studio", ID)
    assert task["kind"] == "architecture" and task["ui_required"] is False
    assert set(task["authorization"]["actions"]) == {"plan", "review", "publish_docs"}
    assert task["scope"]["allowed_paths"] == ["work/items/UI-004-02/"]
    assert task["release_authorization"]["actions"] == []
    result = workflow.check_task(ROOT / "studio", ID, "planning")
    for name in ("ARCHITECTURE.md", "SECURITY.md", "CONTRAT-PROPOSE.md", "RESEARCH.md", "VISUAL-REVIEW.md", "REPORT.md", "EVIDENCE.md"):
        workflow._document(directory, name)
    result["control"] = "complémentaire local, identité/type adaptés en mémoire"
    result["contract_sha256"] = workflow.contract_fingerprint(ROOT / "studio", ID)
    result["additional_documents_checked"] = 7
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

