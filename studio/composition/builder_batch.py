"""Apply the visual workshop's pending gestures against a single locked site revision."""
from copy import deepcopy
from hashlib import sha256
import json
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import transaction

from .appearance_contract import block_lists
from .editor import _FIELDS, _apply, _block_location, _canvas_change, _member
from .models import BuilderSave
from .placement import FORMATS, FORMAT_NAMES, effective_placement
from .services import _current_head, _save, _writing_site
from .validation import MAX_BYTES, MAX_NODES, _check_document, _object, _uuid


MAX_COMMANDS = 128


def _fingerprint(payload):
    _object(payload, "sauvegarde", ("key", "base", "page", "commands"), ("selection",))
    for field in ("key", "base", "page"):
        _uuid(payload[field], field)
    if payload.get("selection") is not None:
        _uuid(payload["selection"], "sélection")
    commands = payload["commands"]
    if not isinstance(commands, list) or len(commands) > MAX_COMMANDS:
        raise ValidationError("Nombre de gestes invalide (128 au maximum).")
    try:
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False,
                         ensure_ascii=False).encode("utf-8")
    except (RecursionError, TypeError, ValueError, UnicodeError):
        raise ValidationError("Contenu de la sauvegarde invalide.") from None
    if len(raw) > MAX_BYTES:
        raise ValidationError("La sauvegarde dépasse la taille autorisée.")
    return sha256(raw).hexdigest()


def _known_ids(document):
    ids = {page["id"] for page in document["pages"]}
    ids.update(section["id"] for page in document["pages"] for section in page["sections"])
    ids.update(block["id"] for _, _, block in block_lists(document))
    return ids


def _remember(mapping, known, local, canonical):
    _uuid(local, "identifiant local")
    if local in mapping or local in known or len(mapping) >= MAX_NODES:
        raise ValidationError("Identifiant local déjà utilisé ou limite des occurrences atteinte.")
    mapping[local] = canonical
    known.add(canonical)


def _subtree(node):
    yield node
    for child in node["children"]:
        yield from _subtree(child)


def _duplicate(page, command, mapping, known):
    _, siblings, source = _block_location(page, command["id"])
    copies = command["local_ids"]
    if not isinstance(copies, dict) or len(copies) > MAX_NODES:
        raise ValidationError("Identifiants de copie invalides.")
    canonical_sources = {mapping.get(key, key): value for key, value in copies.items()}
    clone = deepcopy(source)
    nodes = list(_subtree(clone))
    if len(canonical_sources) != len(copies) or {n["id"] for n in nodes} != canonical_sources.keys():
        raise ValidationError("La copie doit identifier chaque occurrence de son sous-arbre.")
    for node in nodes:
        local = canonical_sources[node["id"]]
        node["id"] = str(uuid4())
        _remember(mapping, known, local, node["id"])
    siblings.insert(siblings.index(source) + 1, clone)
    return clone["id"]


def _collisions(page, identity):
    """For each breakpoint, inspect free siblings of the changed occurrence only."""
    _, siblings, node = _block_location(page, identity)
    collisions = {}
    for fmt in FORMATS:
        box = effective_placement(node.get("placement", {}), fmt)
        if box["mode"] != "free":
            continue
        for other in siblings:
            if other["id"] == identity:
                continue
            peer = effective_placement(other.get("placement", {}), fmt)
            if peer["mode"] != "free":
                continue
            width = min(box["x"] + box["width"], peer["x"] + peer["width"]) - max(box["x"], peer["x"])
            height = min(box["y"] + box["height"], peer["y"] + peer["height"]) - max(box["y"], peer["y"])
            if width > 0 and height > 0:
                collisions[fmt, other["id"]] = (box["z"], peer["z"])
    return collisions


def _command(document, page_id, site_id, raw, mapping, known, previous):
    action = raw.get("action") if isinstance(raw, dict) else None
    if not isinstance(action, str) or action not in (*_FIELDS, "block_duplicate"):
        raise ValidationError("Commande de composition inconnue.")
    required, optional = _FIELDS.get(action, (("id", "local_ids"), ()))
    adding = action in ("section_add", "block_add")
    if adding:
        required += ("local_id",)
    if action == "block_place":
        optional += ("overlap",)
    _object(raw, "geste", ("action", *required), optional)
    command = dict(raw)
    for field in ("id", "parent", "before"):
        if field in command and not (field == "before" and command[field] is None):
            _uuid(command[field], field)
            command[field] = mapping.get(command[field], command[field])

    page = _member(document["pages"], page_id)
    document["schema_version"] = max(3, document["schema_version"])
    moving = action in ("block_place", "block_move")
    before = _collisions(page, command["id"]) if moving else {}
    overlap = command.pop("overlap", False)
    if type(overlap) is not bool or (overlap and
            (not isinstance(command["patch"], dict) or type(command["patch"].get("z")) is not int)):
        raise ValidationError("Précisez explicitement l’ordre de superposition du bloc.")
    if action == "block_duplicate":
        selected = _duplicate(page, command, mapping, known)
    elif action in ("block_place", "parent_layout"):
        selected = _canvas_change(site_id, page, command)
        if action == "block_place" and "placement" in _block_location(page, selected)[2]:
            document["schema_version"] = 4
    else:
        selected = _apply(site_id, page, command)
        if adding:
            _remember(mapping, known, command["local_id"], selected)

    checked = _check_document(document, site_id, None, None, {}, previous, preserve=True)
    if moving or action == "block_duplicate":
        after = _collisions(_member(checked["pages"], page_id), selected)
        for (fmt, other), order in after.items():
            previous_order = before.get((fmt, other))
            new_overlap = previous_order is None
            lost_layer = (order[0] == order[1] and
                          (new_overlap or previous_order[0] != previous_order[1]))
            if (new_overlap and not overlap) or lost_layer:
                raise ValidationError(f"Superposition en {FORMAT_NAMES[fmt]} entre {selected} et {other}.",
                                      code="collision")
    return checked, selected


def _response(receipt):
    return {"revision": str(receipt.revision_id), "number": receipt.revision.number,
            "selection": str(receipt.selection) if receipt.selection else None, "mapping": receipt.mapping}


@transaction.atomic
def save_batch(actor, site_id, payload):
    site = _writing_site(actor, site_id)
    fingerprint = _fingerprint(payload)
    scope = {"operator": actor, "site": site, "key": payload["key"]}
    receipt = BuilderSave.objects.select_related("revision").filter(**scope).first()
    if receipt:
        if receipt.fingerprint != fingerprint:
            raise ValidationError("Cette clé désigne une sauvegarde différente.", code="key_reused")
        return _response(receipt)

    head = _current_head(site, payload["base"])
    document = deepcopy(head.document)
    page_id = payload["page"]
    _member(document["pages"], page_id)
    known = _known_ids(document)
    mapping = {}
    selected = None
    for index, cmd in enumerate(payload["commands"], 1):
        try:
            document, selected = _command(document, page_id, site.pk, cmd, mapping, known, head.document)
        except ValidationError as exc:
            raise ValidationError(f"Geste {index} · {' '.join(exc.messages)}",
                                  code=getattr(exc, "code", "invalid_command")) from exc

    if "selection" in payload:
        selected = mapping.get(payload["selection"], payload["selection"])
    remaining = _known_ids({"pages": [_member(document["pages"], page_id)]})
    if selected not in remaining:
        selected = None
    revision_id, number = str(head.pk), head.number
    if payload["commands"]:
        saved = _save(actor, site, head, document, {}, None)
        revision_id, number = saved["id"], saved["number"]
    BuilderSave.objects.create(**scope, revision_id=revision_id, fingerprint=fingerprint,
                               mapping=mapping, selection=selected)
    return {"revision": revision_id, "number": number, "mapping": mapping, "selection": selected}
