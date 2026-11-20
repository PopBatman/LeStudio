"""Création locale et commandes de structure sur la tête autorisée d’un site."""
import json
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import transaction

from .appearance_contract import AppearanceContract
from .placement import LAYOUT_FIELDS, PLACEMENT_FIELDS, patch_format
from .services import _current_head, _save, _writing_site, creer_brouillon
from .validation import _check_document, _layout, _object


def _template(site_id, origin):
    if origin == {"kind": "template", "ref": "presentation-activite", "version": "1"}:
        path = Path(__file__).parent / "assets" / "presentation-activite-v1.json"
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def creer_atelier(actor, site_id, depart):
    if depart == "blank":
        document = {
            "schema_version": 3, "menus": [], "theme": {},
            "pages": [{"id": str(uuid4()), "title": "Accueil", "slug": "", "parent_id": None, "sections": []}],
        }
        return creer_brouillon(actor, site_id, {"kind": "blank"}, document)
    if depart == "template":
        return creer_brouillon(actor, site_id, {"kind": "template", "ref": "presentation-activite", "version": "1"},
                               resolve_origin=_template)
    with transaction.atomic():
        _writing_site(actor, site_id)
        raise ValidationError("Ce point de départ est indisponible.")


def _member(siblings, node_id):
    for node in siblings:
        if node["id"] == node_id:
            return node
    raise ValidationError("Élément indisponible dans cette sélection.")


def _branches(parent, siblings):
    for block in siblings:
        yield parent, siblings, block
        yield from _branches(block, block["children"])


def _block_location(page, node_id):
    for section in page["sections"]:
        for parent, siblings, block in _branches(section, section["blocks"]):
            if block["id"] == node_id:
                return parent, siblings, block
    raise ValidationError("Occurrence indisponible dans cette page.")


def _container_layout(site_id, node):
    manifest = AppearanceContract(site_id).manifest(node["definition"], "parent", True)
    if manifest["renderer"] != "container":
        raise ValidationError("Choisissez une section ou un conteneur comme destination.")
    # An old component can share the current container key but store different properties.
    props = node["props"]
    _object(props, "conteneur", ("layout",))
    _layout(props["layout"], "disposition du conteneur")
    return props["layout"]


def _destination(site_id, page, parent_id):
    for section in page["sections"]:
        if section["id"] == parent_id:
            return section["blocks"]
    _, _, parent = _block_location(page, parent_id)
    _container_layout(site_id, parent)
    return parent["children"]


def _insert(siblings, node, before):
    index = len(siblings) if before is None else siblings.index(_member(siblings, before))
    siblings.insert(index, node)


def _remove(parent, siblings, node, confirmed):
    if confirmed is not True:
        raise ValidationError("Confirmez le retrait de cet élément et de ses descendants.")
    index = siblings.index(node)
    siblings.pop(index)
    return siblings[min(index, len(siblings) - 1)]["id"] if siblings else parent["id"]


_FIELDS = {
    "section_add": ((), ("before", "layout")),
    "section_edit": (("id", "layout"), ()),
    "section_move": (("id",), ("before",)),
    "section_remove": (("id", "confirmed"), ()),
    "block_add": (("parent", "definition", "props"), ("appearance", "before")),
    "block_edit": (("id", "definition", "props"), ("appearance",)),
    "block_move": (("id", "parent"), ("before",)),
    "block_remove": (("id", "confirmed"), ()),
    "block_place": (("id", "format", "patch"), ("clear", "parent", "before")),
    "parent_layout": (("id", "format", "patch"), ("clear",)),
}


def _canvas_change(site_id, page, command):
    node_id = command["id"]
    fmt, patch, clear = command["format"], command["patch"], command.get("clear", [])
    if command["action"] == "parent_layout":
        for section in page["sections"]:
            if section["id"] == node_id:
                layout = section["layout"]
                break
        else:
            _, _, node = _block_location(page, node_id)
            layout = _container_layout(site_id, node)
        patch_format(layout, fmt, patch, clear, LAYOUT_FIELDS)
    else:
        _, _, node = _block_location(page, node_id)
        placement = node.get("placement", {"base": {}})
        patch_format(placement, fmt, patch, clear, PLACEMENT_FIELDS)
        if placement["base"].get("mode") == "flow":
            del placement["base"]["mode"]
        if placement["base"] or len(placement) > 1:
            node["placement"] = placement
        else:
            node.pop("placement", None)
        if "parent" in command:
            _apply(site_id, page, {"action": "block_move", "id": node_id,
                                   "parent": command["parent"], "before": command.get("before")})
        elif "before" in command:
            raise ValidationError("Choisissez le parent de destination.")
    return node_id


def _apply(site_id, page, command):
    action = command["action"]
    sections = page["sections"]
    before = command.get("before")
    if action == "section_add":
        node = {"id": str(uuid4()), "layout": command.get("layout", {"base": {"display": "stack"}}), "blocks": []}
        _insert(sections, node, before)
    elif action == "block_add":
        siblings = _destination(site_id, page, command["parent"])
        node = {"id": str(uuid4()), "children": []}
        _insert(siblings, node, before)
    else:
        if action.startswith("section_"):
            parent, siblings, node = page, sections, _member(sections, command["id"])
        else:
            parent, siblings, node = _block_location(page, command["id"])
        if action.endswith("_remove"):
            return _remove(parent, siblings, node, command["confirmed"])
        if action.endswith("_move"):
            if before == node["id"] and (action == "section_move" or parent["id"] == command["parent"]):
                if action == "block_move":
                    _destination(site_id, page, command["parent"])
                return node["id"]
            siblings.remove(node)
            # Resolving after detachment excludes both the node and its descendants.
            destination = sections if action == "section_move" else _destination(site_id, page, command["parent"])
            _insert(destination, node, before)
        if action == "section_edit":
            node["layout"] = command["layout"]
    if action in ("block_add", "block_edit"):
        node.update(definition=command["definition"], props=command["props"])
        if "appearance" in command:
            appearance = command["appearance"]
            _object(appearance, "appearance", optional=("variant", "tokens"))
            if appearance:
                node["appearance"] = appearance
            else:
                node.pop("appearance", None)
    return node["id"]


@transaction.atomic
def modifier_structure(actor, site_id, base, command):
    site = _writing_site(actor, site_id)
    head = _current_head(site, base)
    action = command.get("action") if isinstance(command, dict) else None
    if not isinstance(action, str) or action not in _FIELDS:
        raise ValidationError("Commande de structure inconnue.")
    required, optional = _FIELDS[action]
    _object(command, "commande", ("action", "page", *required), optional)
    document = deepcopy(head.document)
    document["schema_version"] = max(3, document["schema_version"])
    page = _member(document["pages"], command["page"])
    if action in ("block_place", "parent_layout"):
        selection = _canvas_change(site.pk, page, command)
        if action == "block_place" and "placement" in _block_location(page, selection)[2]:
            document["schema_version"] = 4
    else:
        selection = _apply(site.pk, page, command)
    checked = _check_document(document, site.pk, None, None, {}, head.document, preserve=True)
    return _save(actor, site, head, checked, {}, None), selection
