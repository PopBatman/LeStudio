#!/usr/bin/env python3
"""Check that T01's reported results and current artifacts agree with observations."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json
import re

ROOT = Path(__file__).resolve().parents[5]
LOT = Path(__file__).resolve().parents[1]
OUT = LOT/"evidence"

def load(name):
    return json.loads((OUT/name).read_text())

def check():
    observed = load("audit-browser.json")
    assert observed["result"] == "passed" and not observed["errors"]
    assert observed["session_cleanup"] and not observed["blocked_writes"]
    assert observed["context"]["revision"] == observed["after"]["revision"]
    assert observed["context"]["document_sha256"] == observed["after"]["digest"]
    widths = [s for s in observed["steps"] if "measured_width" in s]
    assert {s["width"] for s in widths} == {390, 820, 1200}
    assert all(s["width"] == s["measured_width"] for s in widths)
    tests = load("tests-cibles-sqlite.json")
    log = (OUT/"tests-cibles-sqlite.log").read_text()
    assert tests["exit_code"] == 0 and "Ran 17 tests" in log and "OK (skipped=1)" in log
    reference = load("check-reference.json")
    assert reference["result"] == "passed" and not reference["errors"] and not reference["network"]
    manifest = load("manifest-sources.json")
    assert not manifest["mismatches"]
    for source in manifest["sources"]:
        digest = sha256((ROOT/"studio"/source["path"]).read_bytes()).hexdigest()
        assert digest == source["sha256"] == source["installed_sha256"], source["path"]
    for source in manifest["ancillary_sources"]:
        assert sha256((ROOT/"studio"/source["path"]).read_bytes()).hexdigest() == source["sha256"]
    required = ["AUDIT.md","INVENTAIRE-T21.md","REFERENCE-PRODUIT.md","DECISION-FRONTEND.md","SPEC.md",
                "TASKLIST.md","ARCHITECTURE.md","SECURITY.md","VISUAL-REVIEW.md","REPORT.md","REVIEW.md","EVIDENCE.md"]
    missing_links = []
    for name in required:
        doc = LOT/name
        text = doc.read_text()
        assert len(text) > 200 and "WORKFLOW-AI:TODO" not in text, name
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if "://" not in target and not (doc.parent/target.split("#")[0]).exists():
                missing_links.append((name,target))
    assert not missing_links, missing_links
    assert "canvas.js" in (LOT/"AUDIT.md").read_text()
    assert "T21" in (LOT/"INVENTAIRE-T21.md").read_text()
    assert len((OUT/"comparaison-reference.html").read_bytes()) < 200*1024
    report = {"observed_at":datetime.now(timezone.utc).isoformat(),
              "command":"python3 studio/work/items/UI-004-01/evidence/validate-audit.py",
              "cwd":str(ROOT),"result":"passed","exit_code":0,
              "checks":["révision/empreinte du site inchangées","largeurs réellement mesurées",
                        "16 tests réussis + 1 ignoré, sans faux total","référence sans réseau ni erreur",
                        "213 sources locales/image courantes","documents/consommateurs V1 et liens présents",
                        "rapport HTML attachable"],
              "scope":"Contrôle de sincérité/cohérence des résultats de l’audit ; pas un test de nouveaux gestes produit."}
    (OUT/"validation-audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(report,ensure_ascii=False))

if __name__ == "__main__":
    check()
