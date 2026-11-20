#!/usr/bin/env python3
"""Offline structure, JSON and local-file link validation; no permission grants."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_REQUIRED = (
    "README.md", "AGENTS.md", "CLAUDE.md", "install.py", "scripts/workflow.py",
    "scripts/validate_workspace.py", "docs/SESSION-SCOPE.md", "governance/EXECUTION-POLICY.md",
    "governance/AGENT-PERMISSIONS.md", "governance/QUALITY-GATES.md",
    "governance/TESTING-POLICY.md", "governance/SECURITY-POLICY.md",
    "workflows/FEATURE-WORKFLOW.md", "workflows/CONNECTOR-WORKFLOW.md",
    "workflows/COMPONENT-WORKFLOW.md", "templates/TASK.example.json",
)
STUDIO_REQUIRED = ("README.md", "project/PROJECT.md", "docs/ARCHITECTURE-CONTRACTS.md")
_spec = importlib.util.spec_from_file_location("workflow_local_validator", ROOT / "scripts/workflow.py")
workflow = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(workflow)


def _without_code(text: str) -> str:
    result, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            token = match.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            result.append(re.sub(r"`+[^`]*`+", "", line))
    return "\n".join(result)


def _document_paths(root: Path, studio: Path):
    yield from root.rglob("*")
    for name in ("project", "docs", "reference", "work"):
        folder = studio / name
        if folder.is_symlink():
            yield folder
        elif folder.is_dir():
            yield from folder.rglob("*")
    yield studio / "README.md"
    for name in ("README.md", "AGENTS.md", "CLAUDE.md"):
        path = root.parent / name
        if path.exists() or path.is_symlink():
            yield path


def validate(root: Path | str = ROOT) -> list[str]:
    root = workflow._absolute(root)
    workspace = root.parent
    studio = workspace / "studio"
    entry_points = {workspace / name for name in ("README.md", "AGENTS.md", "CLAUDE.md")}
    problems = []
    try:
        workflow._no_links(root)
        workflow._no_links(studio)
    except workflow.WorkflowError as error:
        return [str(error)]
    for directory, required in ((root, WORKFLOW_REQUIRED), (studio, STUDIO_REQUIRED)):
        for name in required:
            path = directory / name
            relative = path.relative_to(workspace)
            try:
                if not workflow._read(path, 2 * 1024 * 1024).strip():
                    problems.append(f"Fichier vide : {relative}")
            except (workflow.WorkflowError, OSError) as error:
                problems.append(f"Fichier requis indisponible : {relative} ({error})")
    for path in _document_paths(root, studio):
        relative = path.relative_to(workspace).as_posix()
        if any(part.startswith(".") or part == "__pycache__" for part in path.relative_to(workspace).parts):
            continue
        if path.is_symlink():
            problems.append(f"Lien symbolique refusé : {relative}")
            continue
        if workflow._private_path(relative):
            problems.append(f"Fichier privé exclu du contrôle : {relative}")
            continue
        if path.suffix not in {".json", ".md"} or not path.is_file():
            continue
        try:
            text = workflow._read(path, 4 * 1024 * 1024).decode("utf-8")
            if path.suffix == ".json":
                json.loads(text)
            else:
                for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", _without_code(text)):
                    raw = match.group(1).strip()
                    if raw.startswith("<") and raw.endswith(">"):
                        raw = raw[1:-1]
                    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", raw) or raw.startswith("#"):
                        continue
                    name = unquote(raw.split("#", 1)[0].split("?", 1)[0])
                    if not name:
                        continue
                    destination = path.parent / name
                    workflow._no_links(destination)
                    resolved = destination.resolve()
                    in_scope = resolved in entry_points or resolved.is_relative_to(root) or resolved.is_relative_to(studio)
                    if not in_scope or not resolved.exists():
                        problems.append(f"Lien local absent ou hors paquet : {relative} -> {raw}")
        except (workflow.WorkflowError, OSError, ValueError, UnicodeError) as error:
            problems.append(f"Fichier invalide : {relative} ({error})")
    try:
        workflow.status(studio)
    except (workflow.WorkflowError, OSError) as error:
        problems.append(f"Liste des tâches invalide ({error})")
    return sorted(set(problems))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Vérifier la structure et les liens locaux ; les SHA du manifeste ne sont pas imposés au dossier de travail évolutif.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    errors = validate()
    result = {"status": "FAIL" if errors else "PASS", "errors": errors,
              "scope": "structure, JSON, schéma des tâches et cibles des liens locaux",
              "notice": "Aucune preuve d’exécution, autorisation, connexion distante ou conformité de Studio n’est établie par ce contrôle."}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for error in errors:
            print("FAIL:", error)
        print(result["status"] + ": " + result["scope"])
        print(result["notice"])
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
