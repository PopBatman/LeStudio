"""Mutations de navigation et bilan des changements dans le brouillon du site."""
from copy import deepcopy
import json
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.utils.crypto import constant_time_compare, salted_hmac

from registre.services import Conflict


class ImpactRequired(Conflict):
    def __init__(self, impact):
        super().__init__("Examinez les conséquences et confirmez votre choix.")
        self.impact = impact


def _invalid(message):
    raise ValidationError(message, code="invalid_navigation")


def _find(rows, key):
    for row in rows:
        if row["id"] == key:
            return row
    _invalid("Élément introuvable dans cette navigation.")


def page_paths(pages):
    by_id = {page["id"]: page for page in pages}
    paths = {}
    for page in pages:
        chain = []
        seen = set()
        current = page
        while current["id"] not in paths:
            if current["id"] in seen:
                _invalid("Une page ne peut pas dépendre de sa descendance.")
            seen.add(current["id"])
            chain.append(current)
            if current["parent_id"] is None:
                break
            current = by_id.get(current["parent_id"])
            if current is None:
                _invalid("La page parente est introuvable.")
        for node in reversed(chain):
            parent = node["parent_id"]
            paths[node["id"]] = "/" if parent is None else paths[parent] + node["slug"] + "/"
    return paths


def _branch(rows, root):
    children = {}
    for row in rows:
        children.setdefault(row["parent_id"], []).append(row["id"])
    found = set()
    pending = [root]
    while pending:
        key = pending.pop()
        if key not in found:
            found.add(key)
            pending.extend(children.get(key, ()))
    return found


def _place(rows, row, parent, before, *, new=False):
    if parent is not None:
        _find(rows, parent)
    if before is not None and _find(rows, before)["parent_id"] != parent:
        _invalid("La position choisie appartient à un autre parent.")
    if not new:
        siblings = [r["id"] for r in rows if r["parent_id"] == parent]
        if row["id"] in siblings:
            following = siblings[siblings.index(row["id"])+1:]
            if before == row["id"] or before == next(iter(following), None):
                return
        rows.remove(row)
    row["parent_id"] = parent
    pos = len(rows) if before is None else rows.index(_find(rows, before))
    rows.insert(pos, row)


def _command_document(original, command):
    if not isinstance(command, dict):
        _invalid("Commande de navigation invalide.")
    document = deepcopy(original)
    document["schema_version"] = max(2, original["schema_version"])
    action = command.get("action")
    if not isinstance(action, str) or action.count("_") != 1:
        _invalid("Action de navigation inconnue.")
    kind, operation = action.split("_")
    if kind not in ("page", "menu", "item") or operation not in ("add", "edit", "move", "delete"):
        _invalid("Action de navigation inconnue.")
    if kind == "item":
        rows = _find(document["menus"], command.get("menu_id"))["items"]
        fields = ("label", "target", "visibility")
    elif kind == "page":
        rows = document["pages"]
        fields = ("title", "slug")
    else:
        rows = document["menus"]
        fields = ("label",)
    row = {"id": str(uuid4())} if operation == "add" else _find(rows, command.get("id"))

    if operation in ("add", "edit"):
        for field in fields:
            if field not in command:
                if operation == "add":
                    _invalid("Champ requis manquant.")
                continue
            row[field] = command[field]
        if operation == "edit":
            return document
        if kind == "menu":
            row["items"] = []
            rows.append(row)
            return document
        if kind == "page":
            row["sections"] = []
    if operation in ("add", "move"):
        if kind == "menu":
            _invalid("Le déplacement concerne les pages et les entrées.")
        if kind == "page" and (not command.get("parent_id") or row.get("parent_id", True) is None):
            _invalid("La racine du site ne peut pas être déplacée ni dupliquée.")
        _place(rows, row, command.get("parent_id") or None, command.get("before_id") or None,
               new=operation == "add")
    elif operation == "delete":
        if kind == "page" and row["parent_id"] is None:
            _invalid("La racine du site doit être conservée.")
        if kind == "menu":
            rows.remove(row)
        else:
            ids = _branch(rows, row["id"])
            if kind == "item" and len(ids) > 1 and command.get("branch") is not True:
                _invalid("Déplacez les enfants ou demandez le retrait de la branche entière.")
            rows[:] = [r for r in rows if r["id"] not in ids]
    return document


def _entries(document):
    return {item["id"]: (menu, item) for menu in document["menus"] for item in menu["items"]}


def navigation_candidate(original, command, decisions):
    candidate = _command_document(original, command)
    if command["action"] != "page_delete":
        return candidate
    remaining = {p["id"] for p in candidate["pages"]}
    for menu in candidate["menus"]:
        removed = set()
        for entry in menu["items"]:
            target = entry["target"]
            if target["kind"] != "page" or target["page_id"] in remaining:
                continue
            decision = decisions.get(entry["id"])
            if decision == "remove":
                removed.add(entry["id"])
            elif decision == "remove_branch":
                removed.update(_branch(menu["items"], entry["id"]))
            elif isinstance(decision, str) and decision in remaining:
                entry["target"] = {"kind": "page", "page_id": decision}
            elif decision:
                _invalid("Choisissez une page de ce brouillon ou le retrait de l’entrée.")
        menu["items"] = [i for i in menu["items"] if i["id"] not in removed]
    return candidate


def check_impact(head, candidate, decisions, confirmation):
    original = head.document
    old_paths = page_paths(original["pages"])
    new_paths = page_paths(candidate["pages"])
    old_root = next(p["id"] for p in original["pages"] if p["parent_id"] is None)
    if new_paths.get(old_root) != "/":
        _invalid("La racine du site doit conserver son identité.")
    changed = {key for key, path in old_paths.items() if new_paths.get(key) != path}
    pages = [dict(id=p["id"], title=p["title"], old_path=old_paths[p["id"]],
                  new_path=new_paths.get(p["id"])) for p in original["pages"] if p["id"] in changed]
    previous = _entries(original)
    current = _entries(candidate)
    entries = []
    removals = []
    expected = set()
    complete = True
    for key, (menu, item) in previous.items():
        target = item["target"]
        if key not in current:
            removals.append(dict(id=key, menu=menu["label"], label=item["label"]))
        if target["kind"] != "page" or target["page_id"] not in changed:
            continue
        page_id = target["page_id"]
        new_target = current[key][1]["target"] if key in current else {}
        children = [e["id"] for e in menu["items"] if e["parent_id"] == key]
        decision = decisions.get(key)
        if page_id not in new_paths:
            expected.add(key)
            if decision in ("remove", "remove_branch"):
                branch = _branch(menu["items"], key) - {key}
                if decision == "remove_branch":
                    valid = key not in current and branch.isdisjoint(current)
                else:
                    # An operator may move children first; never lose them implicitly.
                    valid = key not in current and all(
                        child in current and current[child][1]["parent_id"] != key
                        for child in children
                    )
            else:
                valid = isinstance(decision, str) and decision in new_paths and new_target == {
                    "kind": "page", "page_id": decision}
            complete = complete and valid
        entries.append(dict(id=key, menu_id=menu["id"], menu=menu["label"], label=item["label"],
                            page_id=page_id, old_path=old_paths[page_id],
                            new_path=new_paths.get(new_target.get("page_id")), children=children,
                            decision=decision))
    if decisions.keys() - expected:
        _invalid("Une résolution ne correspond plus aux liens concernés.")
    if not pages and not removals:
        return
    impact = dict(pages=pages, entries=entries, removed_entries=removals, complete=complete)
    message = json.dumps([str(head.pk), candidate, impact], sort_keys=True, separators=(",", ":"))
    token = salted_hmac("studio.navigation.impact", message, algorithm="sha256").hexdigest()
    impact["token"] = token
    if not complete or not isinstance(confirmation, str) or not constant_time_compare(confirmation, token):
        raise ImpactRequired(impact)
