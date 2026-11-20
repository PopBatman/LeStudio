"""Opérations d’apparence sur la tête de brouillon autorisée."""

from copy import deepcopy

from django.core.exceptions import ValidationError
from django.db import transaction

from .appearance_contract import AppearanceContract, block_lists, checked_key, effective_appearance
from .services import _current_head, _save, _writing_site
from .validation import _check_document, _object


def occurrences(document):
    for page, _, block in block_lists(document):
        yield page, block


def diagnostics(site_id, document):
    """Inspect an already authorised revision, including references retained by navigation."""
    contract = AppearanceContract(site_id, document)
    issues = []
    for page, block in occurrences(document):
        message = None
        blocking = False
        try:
            contract.block(page["id"], block, "occurrence")
            ref = block["definition"]
            if contract.manifest(ref, "definition", True)["retired"]:
                message = "Version retirée du catalogue, conservée sur cette occurrence."
        except ValidationError as err:
            message = " ".join(err.messages)
            blocking = True
        if message:
            issues.append(
                {"page_id": page["id"], "block_id": block["id"], "message": message, "blocking": blocking}
            )
    theme = document["theme"]
    try:
        contract.theme({k: v for k, v in theme.items() if k != "components"})
    except ValidationError as err:
        issues.append(
            {"page_id": None, "block_id": None, "message": " ".join(err.messages), "blocking": True}
        )
    for preference in theme.get("components", []):
        try:
            contract.preference(preference, "theme.components")
        except ValidationError as err:
            issues.append(
                {
                    "page_id": None,
                    "block_id": None,
                    "definition": preference["definition"],
                    "message": " ".join(err.messages),
                    "blocking": True,
                }
            )
    return issues


@transaction.atomic
def modifier_apparence(acteur, site_id, revision_de_base, commande):
    site = _writing_site(acteur, site_id)
    head = _current_head(site, revision_de_base)
    document = deepcopy(head.document)
    document["schema_version"] = max(3, document["schema_version"])
    action = commande.get("action") if isinstance(commande, dict) else None
    theme = document["theme"]
    if action == "theme":
        _object(commande, "commande", ("action", "values"))
        values = commande["values"]
        _object(values, "theme", optional=("accent", "background", "ink", "font", "gap", "media"))
        document["theme"] = dict(values)
        if "components" in theme:
            document["theme"]["components"] = theme["components"]
    elif action == "preference":
        _object(commande, "commande", ("action", "definition", "appearance"))
        ref, settings = commande["definition"], commande["appearance"]
        checked_key(ref, "definition")
        _object(settings, "appearance", optional=("variant", "tokens"))
        prefs = list(theme.get("components", ()))
        pos = next((i for i, pref in enumerate(prefs) if pref["definition"] == ref), len(prefs))
        if pos < len(prefs):
            prefs.pop(pos)
        if settings:
            prefs.insert(pos, {"definition": ref, **settings})
        if prefs:
            theme["components"] = prefs
        else:
            theme.pop("components", None)
    elif action in ("block", "remove"):
        match = next(
            (
                (siblings, block)
                for _, siblings, block in block_lists(document)
                if block["id"] == commande.get("id")
            ),
            None,
        )
        if match is None:
            raise ValidationError("Occurrence indisponible dans ce brouillon.")
        siblings, block = match
        if action == "remove":
            _object(commande, "commande", ("action", "id", "confirmed"))
            if commande["confirmed"] is not True:
                raise ValidationError("Confirmez le retrait de l’occurrence et de ses descendants.")
            siblings.remove(block)
        else:
            _object(commande, "commande", ("action", "id", "definition", "props", "appearance"))
            block.update(definition=commande["definition"], props=commande["props"])
            _object(commande["appearance"], "appearance", optional=("variant", "tokens"))
            if commande["appearance"]:
                block["appearance"] = commande["appearance"]
            else:
                block.pop("appearance", None)
    else:
        raise ValidationError("Commande d’apparence inconnue.")
    checked = _check_document(document, site.pk, None, None, {}, head.document, preserve=True)
    return _save(acteur, site, head, checked, {}, None)
