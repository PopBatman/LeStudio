#!/usr/bin/env python3
"""Identify the audit's local inputs and verify their counterparts in the running image."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[5]
STUDIO = ROOT / "studio"
OUT = Path(__file__).resolve().parent
AREAS = ("composition", "registre", "depots", "workspace", "central", "templates", "static/ui", "tests")
SUFFIXES = {".py", ".html", ".js", ".css"}

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def collect():
    paths = sorted({str(p.relative_to(STUDIO)) for area in AREAS
                    for p in (STUDIO / area).rglob("*") if p.is_file() and p.suffix in SUFFIXES})
    assert paths and all(not p.startswith((".", "/")) and ".." not in Path(p).parts for p in paths)
    code = "from pathlib import Path; import hashlib,json; paths=" + repr(paths) + "; print(json.dumps({p:hashlib.sha256((Path('/app')/p).read_bytes()).hexdigest() if (Path('/app')/p).is_file() else None for p in paths}))"
    command = ["docker", "compose", "-f", "studio/compose.yaml", "exec", "-T", "web", "python", "-c", code]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True)
    installed = json.loads(result.stdout)
    records = [{"path":p, "sha256":digest(STUDIO/p), "installed_sha256":installed[p]} for p in paths]
    mismatches = [r["path"] for r in records if r["sha256"] != r["installed_sha256"]]
    extras = ["frontend/package.json", "frontend/package-lock.json", "frontend/gallery.css", "requirements.txt",
              "engine/requirements.in", "engine/reference/preview.py", "engine/reference/templates/reference/preview_blocks.html",
              "Dockerfile", ".dockerignore", ".gitlab-ci.yml", "compose.yaml", "local.env.example",
              "docs/BROUILLONS.md", "docs/MOTEUR-WAGTAIL.md"]
    ancillary = [{"path":p, "sha256":digest(STUDIO/p)} for p in extras if (STUDIO/p).is_file()]
    report = {"observed_at":datetime.now(timezone.utc).isoformat(),
              "command":"python3 studio/work/items/UI-004-01/evidence/collect-sources.py",
              "cwd":str(ROOT), "subprocess_command":command,
              "scope":"Sources locales de composition, accès, rendus, templates, assets et tests comparées au /app exécuté ; aucun secret/configuration privée lu.",
              "sources":records, "ancillary_sources":ancillary, "mismatches":mismatches,
              "result":"passed" if not mismatches else "failed",
              "limit":"Les autres sources moteur/configuration ne sont pas prétendues comparées à leur instance par ce contrôle."}
    (OUT/"manifest-sources.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    assert not mismatches, "Sources différentes de l'image : "+", ".join(mismatches)
    print(json.dumps({"matched_sources":len(records), "ancillary_sources":len(ancillary), "result":report["result"]}))

if __name__ == "__main__":
    collect()
