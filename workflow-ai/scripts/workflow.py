#!/usr/bin/env python3
"""Local documentary checks. This is not an authorization server or agent runtime."""
from __future__ import annotations

import argparse
from datetime import datetime
import fnmatch
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile

WORKFLOW_ROOT = Path(__file__).resolve().parents[1]
STUDIO_ROOT = WORKFLOW_ROOT.parent / "studio"
TASK_ID = re.compile(r"^(FEAT|CONN|UI|ARCH)-[0-9]{3,6}$")
PREFIX = {"feature": "FEAT", "connector": "CONN", "component": "UI", "architecture": "ARCH"}
STATES = {"DRAFT", "DISCOVERY", "SPECIFIED", "PLANNED", "READY", "IMPLEMENTING", "VERIFIED", "REVIEWED", "DONE"}
KINDS = {"test", "integration", "screenshot", "mockup", "review", "manual", "deployment"}
ACTIONS = {"plan", "implement", "test", "review", "publish_docs", "release"}
PHASES = ("planning", "implementation", "verification", "release")
TODO = "<!-- WORKFLOW-AI:TODO -->"
BASE_DOCS = ("SPEC.md", "TASKLIST.md", "ARCHITECTURE.md", "SECURITY.md")
MAX_READ = 20 * 1024 * 1024
HEX = re.compile(r"^[a-f0-9]{64}$")
NOTICE = ("Contrôle documentaire local : les références d’autorisation et d’indépendance sont déclaratives. "
          "Ce résultat n’authentifie personne, ne change aucun état et ne bloque pas les accès directs du runtime.")


class WorkflowError(ValueError):
    pass


def _absolute(path: Path | str) -> Path:
    return Path(os.path.abspath(os.path.expanduser(str(path))))


def _no_links(path: Path) -> None:
    for part in (path, *path.parents):
        if part.is_symlink():
            raise WorkflowError(f"Lien symbolique refusé : {part}")


def _relative(value: object, *, patterns: bool = False) -> str:
    if not isinstance(value, str) or not value or len(value) > 1000:
        raise WorkflowError("Chemin relatif invalide.")
    if "\\" in value or any(ord(c) < 32 for c in value):
        raise WorkflowError("Chemin relatif invalide.")
    stripped = value.rstrip("/") if patterns else value
    if not stripped or PurePosixPath(stripped).is_absolute() or any(p in {"", ".", ".."} for p in stripped.split("/")):
        raise WorkflowError("Chemin absolu ou traversée refusés.")
    if len(stripped.split("/")) > 100:
        raise WorkflowError("Chemin trop profond.")
    if not patterns and any(c in value for c in "*?[]"):
        raise WorkflowError("Un artefact doit avoir un chemin exact.")
    return stripped


def _private_path(value: str) -> bool:
    parts = tuple(p.casefold() for p in PurePosixPath(value).parts)
    return any(p in {".git", ".ssh", ".aws", ".azure", ".gnupg"}
               or p.startswith(".env") or p in {"credentials", "credentials.json", "secrets.json", "secrets.yaml", "auth.json"}
               for p in parts) or PurePosixPath(value).suffix.lower() in {".key", ".pem", ".p12", ".pfx"}


def _read(path: Path, maximum: int = MAX_READ) -> bytes:
    _no_links(path)
    if not path.is_file() or path.stat().st_size > maximum:
        raise WorkflowError(f"Fichier absent, non régulier ou trop volumineux : {path.name}")
    with path.open("rb") as handle:
        data = handle.read(maximum + 1)
    if len(data) > maximum:
        raise WorkflowError("Fichier trop volumineux.")
    return data


def _sha(path: Path) -> str:
    return hashlib.sha256(_read(path)).hexdigest()


def task_directory(root: Path | str, task_id: str) -> Path:
    if not isinstance(task_id, str) or not TASK_ID.fullmatch(task_id):
        raise WorkflowError("Identifiant attendu : FEAT-001, CONN-001, UI-001 ou ARCH-001.")
    path = _absolute(root) / "work" / "items" / task_id
    _no_links(path)
    return path


def _text(value: object, label: str, *, nullable: bool = False) -> None:
    if value is None and nullable:
        return
    if not isinstance(value, str) or not value.strip() or len(value) > 2000 or "\x00" in value:
        raise WorkflowError(f"{label} doit être une chaîne non vide.")


def _authorization(value: object, label: str) -> None:
    if not isinstance(value, dict):
        raise WorkflowError(f"{label} doit être un objet.")
    _text(value.get("reference"), label + ".reference", nullable=True)
    actions = value.get("actions")
    if not isinstance(actions, list) or any(not isinstance(x, str) or x not in ACTIONS for x in actions):
        raise WorkflowError(f"Actions invalides dans {label}.")


def load_task(root: Path | str, task_id: str) -> tuple[Path, dict]:
    directory = task_directory(root, task_id)
    try:
        task = json.loads(_read(directory / "task.json", 1024 * 1024))
    except (ValueError, UnicodeError):
        raise WorkflowError("task.json est absent ou invalide.") from None
    if (not isinstance(task, dict) or type(task.get("schema_version")) is not int
            or task.get("schema_version") != 1 or task.get("id") != task_id):
        raise WorkflowError("Schéma ou identité de tâche invalide.")
    kind = task.get("kind")
    if not isinstance(kind, str) or kind not in PREFIX or not task_id.startswith(PREFIX[kind] + "-"):
        raise WorkflowError("Le type de tâche ne correspond pas au préfixe de son identifiant.")
    _text(task.get("title"), "title")
    if not isinstance(task.get("state"), str) or task.get("state") not in STATES or type(task.get("ui_required")) is not bool:
        raise WorkflowError("État ou ui_required invalide.")
    if kind == "component" and task["ui_required"] is not True:
        raise WorkflowError("Une tâche component exige ui_required=true.")
    scope = task.get("scope")
    if not isinstance(scope, dict):
        raise WorkflowError("scope doit être un objet.")
    for key in ("allowed_paths", "forbidden_paths"):
        values = scope.get(key)
        if not isinstance(values, list) or len(values) > 200:
            raise WorkflowError(f"scope.{key} doit être une liste de chemins.")
        for value in values:
            _relative(value, patterns=True)
    _authorization(task.get("authorization"), "authorization")
    _authorization(task.get("release_authorization", {"reference": None, "actions": []}), "release_authorization")
    review = task.get("review", {"reference": None, "independent": False})
    if not isinstance(review, dict) or type(review.get("independent")) is not bool:
        raise WorkflowError("review invalide.")
    _text(review.get("reference"), "review.reference", nullable=True)
    if not isinstance(task.get("evidence"), list) or len(task["evidence"]) > 100:
        raise WorkflowError("evidence doit être une liste bornée.")
    return directory, task


def path_matches(path: str, pattern: str) -> bool:
    """Component-wise glob: ** matches zero or more directories; plain paths include descendants."""
    path, pattern = _relative(path), _relative(pattern, patterns=True)
    if not any(c in pattern for c in "*?["):
        return path == pattern or path.startswith(pattern + "/")
    names, pats = path.split("/"), pattern.split("/")

    @lru_cache(maxsize=None)
    def match(i: int, j: int) -> bool:
        if j == len(pats):
            return i == len(names)
        if pats[j] == "**":
            return match(i, j + 1) or (i < len(names) and match(i + 1, j))
        return i < len(names) and fnmatch.fnmatchcase(names[i], pats[j]) and match(i + 1, j + 1)
    return match(0, 0)


def scope_allows(scope: dict, path: str) -> bool:
    return (not _private_path(path)
            and not any(path_matches(path, rule) for rule in scope["forbidden_paths"])
            and any(path_matches(path, rule) for rule in scope["allowed_paths"]))


def _document(directory: Path, name: str) -> bytes:
    raw = _read(directory / name, 2 * 1024 * 1024)
    try:
        text = raw.decode("utf-8")
    except UnicodeError:
        raise WorkflowError(f"Document non UTF-8 : {name}") from None
    if not text.strip() or TODO in text:
        raise WorkflowError(f"Document vide ou encore à compléter : {name}")
    return raw


def contract_fingerprint(root: Path | str, task_id: str) -> str:
    directory, task = load_task(root, task_id)
    names = list(BASE_DOCS) + (["VISUAL-REVIEW.md"] if task["ui_required"] else [])
    records = [{"path": name, "sha256": hashlib.sha256(_document(directory, name)).hexdigest()} for name in names]
    return hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _check_evidence(directory: Path, evidence: dict, task: dict, project: Path) -> None:
    if (not isinstance(evidence, dict) or not isinstance(evidence.get("kind"), str)
            or evidence.get("kind") not in KINDS):
        raise WorkflowError("Type de preuve invalide.")
    active = evidence.get("active", True)
    if type(active) is not bool:
        raise WorkflowError("evidence.active doit être un booléen.")
    relative = _relative(evidence.get("path"))
    if not relative.startswith("evidence/") or _private_path(relative):
        raise WorkflowError("Une preuve doit être un artefact non secret sous evidence/.")
    digest = evidence.get("sha256")
    if not isinstance(digest, str) or not HEX.fullmatch(digest) or _sha(directory / relative) != digest:
        raise WorkflowError(f"Empreinte de preuve absente ou périmée : {relative}")
    timestamp = evidence.get("observed_at")
    try:
        instant = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        if instant.tzinfo is None:
            raise ValueError("timezone missing")
    except (ValueError, AttributeError, TypeError):
        raise WorkflowError("observed_at doit être une date ISO avec fuseau.") from None
    _text(evidence.get("revision"), "evidence.revision")
    if (not isinstance(evidence.get("outcome"), str)
            or evidence.get("outcome") not in {"passed", "failed", "not_run", "illustrative"}):
        raise WorkflowError("outcome invalide.")
    contract = evidence.get("contract_sha256")
    if contract is not None and (not isinstance(contract, str) or not HEX.fullmatch(contract)):
        raise WorkflowError("contract_sha256 invalide.")
    inputs = evidence.get("inputs", [])
    if not isinstance(inputs, list) or len(inputs) > 200:
        raise WorkflowError("inputs doit être une liste bornée.")
    seen = set()
    for item in inputs:
        if not isinstance(item, dict):
            raise WorkflowError("Entrée source invalide.")
        name = _relative(item.get("path"))
        if name in seen or _private_path(name) or (active and not scope_allows(task["scope"], name)):
            raise WorkflowError(f"Entrée source hors périmètre ou dupliquée : {name}")
        seen.add(name)
        digest = item.get("sha256")
        if not isinstance(digest, str) or not HEX.fullmatch(digest):
            raise WorkflowError(f"Empreinte source invalide : {name}")
        if active and _sha(project / name) != digest:
            raise WorkflowError(f"Preuve périmée : empreinte source différente pour {name}")


def check_task(root: Path | str, task_id: str, phase: str, *, project_root: Path | str | None = None) -> dict:
    if phase not in PHASES:
        raise WorkflowError("Phase inconnue.")
    root = _absolute(root)
    project = _absolute(project_root if project_root is not None else root)
    _no_links(project)
    directory, task = load_task(root, task_id)
    rank = PHASES.index(phase)
    names = ["SPEC.md", "TASKLIST.md"]
    if rank >= 1:
        names += ["ARCHITECTURE.md", "SECURITY.md"]
        auth = task["authorization"]
        if not auth.get("reference") or "implement" not in auth["actions"]:
            raise WorkflowError("Référence de mandat et action 'implement' requises ; aucun accord n’est déduit du statut.")
        if not task["scope"]["allowed_paths"]:
            raise WorkflowError("Le périmètre de modification doit être explicitement renseigné.")
        if task["ui_required"]:
            names += ["VISUAL-REVIEW.md"]
    if rank >= 2:
        names += ["REPORT.md"]
    if rank >= 3:
        names += ["REVIEW.md"]
        review = task.get("review", {})
        auth = task.get("release_authorization", {})
        if not review.get("reference") or review.get("independent") is not True:
            raise WorkflowError("Référence de revue indépendante requise (authenticité à contrôler par le runtime).")
        if not auth.get("reference") or "release" not in auth.get("actions", []):
            raise WorkflowError("Référence de mandat et action 'release' requises.")
    for name in names:
        _document(directory, name)
    for evidence in task["evidence"]:
        _check_evidence(directory, evidence, task, project)
    evidence = task["evidence"]
    if rank >= 1 and task["ui_required"] and not any(
            item["kind"] == "mockup" and item.get("active", True)
            and item["outcome"] in {"illustrative", "passed"} for item in evidence):
        raise WorkflowError("Référence de maquette requise avant une implémentation frontend.")
    if rank >= 2:
        fingerprint = contract_fingerprint(root, task_id)
        required = ["test"] + (["screenshot"] if task["ui_required"] else []) + (["review"] if rank >= 3 else [])
        for kind in required:
            active = [item for item in evidence if item["kind"] == kind and item.get("active", True)]
            if not active or any(item["outcome"] != "passed" or not item.get("inputs")
                                 or item.get("contract_sha256") != fingerprint for item in active):
                raise WorkflowError(f"Toutes les preuves actives '{kind}' doivent être passées, liées au contrat et aux sources courantes ; au moins une est requise.")
    return {"task": task_id, "phase": phase, "status": "PASS", "state_unchanged": task["state"],
            "documents_checked": names, "evidence_checked": len(evidence), "notice": NOTICE}


def new_task(root: Path | str, task_id: str, kind: str, title: str, *, ui: bool = False) -> Path:
    root = _absolute(root)
    destination = task_directory(root, task_id)
    if kind not in PREFIX or not task_id.startswith(PREFIX[kind] + "-"):
        raise WorkflowError("Le type et le préfixe de l’identifiant ne correspondent pas.")
    _text(title, "title")
    if len(title) > 240:
        raise WorkflowError("Titre trop long (240 caractères maximum).")
    if destination.exists():
        raise WorkflowError("Cette tâche existe déjà ; aucune donnée modifiée.")
    ui = bool(ui or kind == "component")
    task = {"schema_version": 1, "id": task_id, "kind": kind, "title": title, "state": "DRAFT",
            "ui_required": ui, "scope": {"allowed_paths": [], "forbidden_paths": [".git/**", ".env", ".env.*"]},
            "authorization": {"reference": None, "actions": []}, "evidence": [],
            "review": {"reference": None, "independent": False},
            "release_authorization": {"reference": None, "actions": []}}
    spec_template = {"feature": "FEATURE-SPEC.md", "connector": "CONNECTOR-SPEC.md",
                     "component": "COMPONENT-SPEC.md", "architecture": "ARCHITECTURE.md"}[kind]
    docs = {"SPEC.md": spec_template, "TASKLIST.md": "TASKLIST.md", "ARCHITECTURE.md": "ARCHITECTURE.md",
            "SECURITY.md": "SECURITY.md", "REPORT.md": "REPORT.md", "REVIEW.md": "REVIEW.md"}
    if ui:
        docs["VISUAL-REVIEW.md"] = "VISUAL-REVIEW.md"
    payload = {}
    for name, template in docs.items():
        candidate = WORKFLOW_ROOT / "templates" / template
        body = _read(candidate, 2 * 1024 * 1024).decode("utf-8")
        payload[name] = f"{TODO}\n\nTâche : {task_id}. Retirer le marqueur uniquement après rédaction.\n\n" + body.replace(TODO, "")
    parent = destination.parent
    _no_links(parent)
    parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".new-task-", dir=parent))
    try:
        (temporary / "evidence").mkdir()
        (temporary / "task.json").write_text(json.dumps(task, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for name, body in payload.items():
            (temporary / name).write_text(body, encoding="utf-8")
        if destination.exists() or destination.is_symlink():
            raise WorkflowError("La destination a été créée en parallèle ; aucun écrasement.")
        temporary.rename(destination)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return destination


def status(root: Path | str) -> list[dict]:
    folder = _absolute(root) / "work" / "items"
    _no_links(folder)
    if not folder.exists():
        return []
    result = []
    for path in sorted(folder.iterdir()):
        if path.is_symlink():
            raise WorkflowError("Lien symbolique refusé dans la liste des tâches.")
        if path.is_dir() and TASK_ID.fullmatch(path.name):
            _, item = load_task(root, path.name)
            result.append({key: item[key] for key in ("id", "kind", "title", "state", "ui_required")})
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Workflow AI : tâches et contrôles documentaires locaux, sans exécution d’agent ni déploiement.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="Lister les états déclarés sans les modifier")
    create = sub.add_parser("new", help="Créer une tâche DRAFT et des modèles à compléter")
    create.add_argument("--id", required=True)
    create.add_argument("--kind", required=True, choices=tuple(PREFIX))
    create.add_argument("--title", required=True)
    create.add_argument("--ui", action="store_true")
    check = sub.add_parser("check", help="Contrôler les documents, mandats déclarés et empreintes ; jamais accorder de droits")
    check.add_argument("--id", required=True)
    check.add_argument("--phase", required=True, choices=PHASES)
    check.add_argument("--project-root", help="Racine des chemins source des preuves (par défaut, studio/)")
    finger = sub.add_parser("fingerprint", help="Calculer l’empreinte des documents du contrat courant")
    finger.add_argument("--id", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "status":
            result = {"tasks": status(STUDIO_ROOT), "notice": NOTICE}
        elif args.command == "new":
            result = {"created": str(new_task(STUDIO_ROOT, args.id, args.kind, args.title, ui=args.ui)), "state": "DRAFT"}
        elif args.command == "check":
            result = check_task(STUDIO_ROOT, args.id, args.phase, project_root=args.project_root)
        else:
            result = {"task": args.id, "contract_sha256": contract_fingerprint(STUDIO_ROOT, args.id)}
    except (WorkflowError, OSError, UnicodeError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error), "notice": NOTICE}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
