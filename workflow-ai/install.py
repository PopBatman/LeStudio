#!/usr/bin/env python3
"""Install the Workflow AI files locally. No network, shell or application setup."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MAX_FILE_BYTES = 16 * 1024 * 1024
MAX_PACKAGE_BYTES = 128 * 1024 * 1024
START = b"<!-- workflow-ai:begin -->"
END = b"<!-- workflow-ai:end -->"
LEGACY_BLOCK = (
    START + b"\n"
    + "## Workflow AI — Studio\n\n"
      "Lire `workflow-ai/AGENTS.md`, puis `workflow-ai/README.md` avant de travailler sur Studio.\n"
      "Le cadre du projet est dans `workflow-ai/project/PROJECT.md` ; le périmètre courant est dans\n"
      "`workflow-ai/project/SESSION-SCOPE.md`. Les mandats utilisateur et règles du runtime priment.\n"
      "Les contrôles locaux du workflow ne donnent aucun droit supplémentaire.\n".encode("utf-8")
    + END + b"\n"
)
BLOCK = (
    START + b"\n"
    + "## Workflow AI — Studio\n\n"
      "Lire `workflow-ai/AGENTS.md` pour les règles de travail et `workflow-ai/README.md` pour les outils.\n"
      "Le projet Django/Wagtail et ses documents se trouvent dans `studio/`, avec `studio/README.md` comme point d’entrée.\n".encode("utf-8")
    + END + b"\n"
)


class InstallError(ValueError):
    """A local, safe-to-display installation error."""


def _absolute(path: Path | str) -> Path:
    return Path(os.path.abspath(os.path.expanduser(str(path))))


def _no_links(path: Path) -> None:
    for part in (path, *path.parents):
        if part.is_symlink():
            raise InstallError(f"Lien symbolique refusé : {part}. Utiliser un chemin physique.")


def _relative(value: object) -> str:
    if not isinstance(value, str) or not value or len(value) > 1000:
        raise InstallError("Chemin de manifeste invalide.")
    if "\\" in value or any(ord(c) < 32 for c in value):
        raise InstallError("Chemin de manifeste invalide.")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in {"", ".", ".."} for p in value.split("/")):
        raise InstallError("Le manifeste doit contenir des chemins relatifs sans traversée.")
    if any(p.casefold() in {".git", ".ssh", ".aws", ".azure", ".gnupg", "__pycache__",
                            "credentials", "credentials.json", "secrets.json", "secrets.yaml", "auth.json"}
           or p.casefold().startswith(".env") for p in path.parts):
        raise InstallError("Le manifeste contient un chemin privé ou un cache interdit.")
    if path.suffix.lower() in {".pyc", ".pyo", ".pem", ".key", ".p12", ".pfx"}:
        raise InstallError("Le manifeste contient un fichier privé ou compilé interdit.")
    return value


def _read(path: Path, maximum: int = MAX_FILE_BYTES) -> bytes:
    _no_links(path)
    if not path.is_file() or not stat.S_ISREG(path.stat().st_mode):
        raise InstallError(f"Fichier régulier requis : {path}")
    if path.stat().st_size > maximum:
        raise InstallError(f"Fichier trop volumineux : {path}")
    with path.open("rb") as handle:
        data = handle.read(maximum + 1)
    if len(data) > maximum:
        raise InstallError(f"Fichier trop volumineux : {path}")
    return data


def load_package(source: Path | str) -> tuple[dict, list[tuple[str, bytes]]]:
    source = _absolute(source)
    _no_links(source)
    if not source.is_dir():
        raise InstallError("Dossier source introuvable.")
    raw = _read(source / "MANIFEST.json", 2 * 1024 * 1024)
    try:
        manifest = json.loads(raw)
    except (ValueError, UnicodeError):
        raise InstallError("MANIFEST.json n’est pas un JSON valide.") from None
    if (not isinstance(manifest, dict) or type(manifest.get("schema_version")) is not int
            or manifest.get("schema_version") not in {1, 2}
            or manifest.get("package") != "workflow-ai-studio"
            or not isinstance(manifest.get("version"), str)):
        raise InstallError("Format de MANIFEST.json non pris en charge.")
    groups = [("workflow-ai", source, manifest.get("files"))]
    if manifest["schema_version"] == 2:
        groups.append(("studio", source.parent / "studio", manifest.get("project_files")))
    elif "project_files" in manifest:
        raise InstallError("La liste des fichiers produit nécessite le format de manifeste 2.")
    if any(not isinstance(records, list) or not records for _, _, records in groups):
        raise InstallError("Le manifeste doit lister les fichiers de chaque dossier.")
    if sum(len(records) for _, _, records in groups) > 2000:
        raise InstallError("Le manifeste contient trop de fichiers.")
    result, seen, total = [], set(), len(raw)
    entries = ((folder, root, record) for folder, root, records in groups for record in records)
    for folder, root, record in entries:
        if not isinstance(record, dict):
            raise InstallError("Entrée de manifeste invalide.")
        name = _relative(record.get("path"))
        relative = f"{folder}/{name}"
        key = relative.casefold()
        if key == "workflow-ai/manifest.json" or key in seen:
            raise InstallError("Chemin dupliqué ou réservé dans le manifeste.")
        seen.add(key)
        digest, size = record.get("sha256"), record.get("size_bytes")
        if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
            raise InstallError(f"Empreinte invalide : {name}")
        if type(size) is not int or size < 0 or size > MAX_FILE_BYTES:
            raise InstallError(f"Taille invalide : {name}")
        data = _read(root / name)
        if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
            raise InstallError(f"Intégrité du paquet non vérifiée : {relative}")
        total += len(data)
        if total > MAX_PACKAGE_BYTES:
            raise InstallError("Paquet trop volumineux.")
        result.append((relative, data))
    names = {n for n, _ in result}
    if not {"workflow-ai/README.md", "workflow-ai/AGENTS.md", "workflow-ai/CLAUDE.md"}.issubset(names):
        raise InstallError("Le manifeste ne contient pas les points d’entrée du workflow.")
    if manifest["schema_version"] == 2 and "studio/README.md" not in names:
        raise InstallError("Le manifeste ne contient pas le point d’entrée du projet Studio.")
    result.append(("workflow-ai/MANIFEST.json", raw))
    return manifest, result


def _bridge(existing: bytes | None, block: bytes) -> bytes:
    if existing is None:
        return block
    starts, ends = existing.count(START), existing.count(END)
    if starts == ends == 0:
        separator = b"" if not existing else (b"\n" if existing.endswith(b"\n") else b"\n\n")
        return existing + separator + block
    if starts != 1 or ends != 1:
        raise InstallError("Bloc Workflow AI incomplet ou dupliqué dans les instructions existantes.")
    left, right = existing.index(START), existing.index(END) + len(END)
    if right < left or existing[left:right] != block.rstrip(b"\n"):
        raise InstallError("Bloc Workflow AI modifié : fusion manuelle requise, aucun écrasement.")
    return existing


def plan_install(source: Path | str, target: Path | str) -> dict:
    source, target = _absolute(source), _absolute(target)
    _no_links(source)
    _no_links(target)
    if target.exists() and not target.is_dir():
        raise InstallError("La cible doit être un dossier.")
    manifest, files = load_package(source)
    split_layout = manifest["schema_version"] == 2
    roots = {"workflow-ai": source}
    if split_layout:
        roots["studio"] = source.parent / "studio"
        for directory in (target, *target.parents):
            if directory.name == "studio" and (directory.parent / "workflow-ai/MANIFEST.json").is_file():
                raise InstallError("Choisir l’espace parent du projet studio/ comme cible.")
    for source_name, source_root in roots.items():
        if target.is_relative_to(source_root):
            raise InstallError(f"Choisir la racine de l’espace, hors du dossier source {source_name}/.")
        for folder in roots:
            destination = target / folder
            if source_root.is_relative_to(destination) and (source_name != folder or source_root != destination):
                raise InstallError("Le paquet source ne peut pas être imbriqué dans sa destination.")
    planned = []

    def add(path: Path, data: bytes, bridge: bool = False) -> None:
        _no_links(path)
        for parent in path.parents:
            if parent.exists() and not parent.is_dir():
                raise InstallError(f"Un parent n’est pas un dossier : {parent}")
        current = _read(path) if path.exists() else None
        desired = _bridge(current, data) if bridge else data
        if current is not None and current != desired and not bridge:
            raise InstallError(f"Conflit : {path}. Fichier conservé ; fusion manuelle requise.")
        planned.append({"path": path, "data": desired, "before": current,
                        "action": "unchanged" if current == desired else "write"})

    for relative, data in files:
        add(target / relative, data)
    block = BLOCK if split_layout else LEGACY_BLOCK
    add(target / "AGENTS.md", block, bridge=True)
    add(target / "CLAUDE.md", block, bridge=True)
    return {"version": manifest["version"], "target": target, "entries": planned}


def install(source: Path | str, target: Path | str, *, apply: bool = False) -> dict:
    plan = plan_install(source, target)
    writes = [entry for entry in plan["entries"] if entry["action"] == "write"]
    created_dirs, completed = [], []
    if apply:
        try:
            for entry in writes:
                path = entry["path"]
                _no_links(path)
                observed = _read(path) if path.exists() else None
                if observed != entry["before"]:
                    raise InstallError("La cible a changé pendant l’installation ; relancer le plan.")
                missing = []
                parent = path.parent
                while not parent.exists():
                    missing.append(parent)
                    parent = parent.parent
                for directory in reversed(missing):
                    _no_links(directory)
                    directory.mkdir()
                    created_dirs.append(directory)
                fd, temporary = tempfile.mkstemp(prefix=".workflow-install-", dir=path.parent)
                try:
                    with os.fdopen(fd, "wb") as handle:
                        handle.write(entry["data"])
                        handle.flush()
                        os.fsync(handle.fileno())
                    _no_links(path)
                    if entry["before"] is None:
                        # Publishing via a hard link is atomic and refuses an existing
                        # destination. A failed write/fsync only leaves the temporary,
                        # removed below; it never exposes a truncated package file.
                        os.link(temporary, path)
                    else:
                        mode = stat.S_IMODE(path.stat().st_mode)
                        os.chmod(temporary, mode)
                        if _read(path) != entry["before"]:
                            raise InstallError("Les instructions ont changé ; fusion interrompue.")
                        os.replace(temporary, path)
                finally:
                    Path(temporary).unlink(missing_ok=True)
                completed.append(entry)
        except BaseException:
            # Best-effort rollback of our own writes; do not undo a concurrent edit.
            for entry in reversed(completed):
                try:
                    path = entry["path"]
                    if not path.is_symlink() and path.is_file() and _read(path) == entry["data"]:
                        if entry["before"] is None:
                            path.unlink()
                        else:
                            path.write_bytes(entry["before"])
                except (OSError, InstallError):
                    pass
            for directory in reversed(created_dirs):
                try:
                    directory.rmdir()
                except OSError:
                    pass
            raise
    return {"mode": "applied" if apply else "dry-run", "version": plan["version"],
            "target": str(plan["target"]), "writes": len(writes),
            "unchanged": len(plan["entries"]) - len(writes),
            "files": [str(entry["path"]) for entry in writes]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Installer local du Workflow AI ; simulation par défaut.")
    parser.add_argument("--target", required=True, help="Racine de l’espace qui contiendra workflow-ai/ et studio/")
    parser.add_argument("--apply", action="store_true", help="Appliquer après le contrôle intégral des conflits")
    args = parser.parse_args(argv)
    try:
        result = install(ROOT, args.target, apply=args.apply)
    except (InstallError, OSError, UnicodeError) as error:
        print(f"ERREUR : {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("Aucun accès réseau, paquet Python, configuration de runtime ou code Studio installé.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
