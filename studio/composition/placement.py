"""Placement local au parent, projeté indépendamment pour chaque format."""

from django.core.exceptions import ValidationError

from .validation import _integer, _invalid, _object

FORMAT_NAMES = {"base": "Bureau", "tablet": "Tablette", "mobile": "Mobile"}
FORMATS = tuple(FORMAT_NAMES)
BOUNDS = {
    "x": (0, 99), "y": (0, 4095), "width": (1, 100), "height": (1, 4096),
    "span": (1, 12), "z": (0, 100),
}
PLACEMENT_FIELDS = ("mode", *BOUNDS)
LAYOUT_FIELDS = ("display", "columns", "gap")


def effective_layout(layout, fmt):
    return {"display": "stack", "columns": 1, "gap": 0,
            **layout.get("base", {}), **layout.get(fmt, {})}


def effective_placement(placement, fmt):
    base = placement.get("base", {})
    local = placement.get(fmt, {})
    base_mode = base.get("mode", "flow")
    mode = local.get("mode", base_mode)
    # A mobile block returned to the flow must not inherit its desktop absolute box.
    effective = {**(base if mode == base_mode else {}), **local}
    if mode == "free":
        return {"mode": mode, "z": 0, **{k: effective[k] for k in ("x", "y", "width", "height", "z")
                                        if k in effective}}
    return {"mode": mode, "span": 1, **{k: effective[k] for k in ("width", "height", "span") if k in effective}}


def placement_error(fmt, block_id, key, message):
    raise ValidationError(f"{FORMAT_NAMES[fmt]} · bloc {block_id} · {message}",
                          code="invalid_document", params={"format": fmt, "field": key, "block": block_id})


def validate_placement(placement, layout, parent_placement, path, block_id):
    _object(placement, path, ("base",), FORMATS[1:])
    for fmt, delta in placement.items():
        field = f"{path}.{fmt}"
        _object(delta, field, optional=PLACEMENT_FIELDS)
        if "mode" in delta and delta["mode"] not in ("flow", "free"):
            _invalid(field + ".mode")
        for key in delta.keys() & BOUNDS.keys():
            _integer(delta[key], field + "." + key, *BOUNDS[key])
    for fmt in FORMATS:
        rules = effective_placement(placement, fmt)
        if rules["mode"] == "flow":
            parent = effective_layout(layout, fmt)
            if rules["span"] > parent["columns"]:
                placement_error(fmt, block_id, "span", "Le bloc occupe plus de colonnes que son parent.")
            continue
        for key in ("x", "y", "width", "height"):
            if key not in rules:
                labels = {"x": "la position X", "y": "la position Y", "width": "la largeur", "height": "la hauteur"}
                placement_error(fmt, block_id, key, f"Renseignez {labels[key]} pour le placement libre.")
        if rules["x"] + rules["width"] > 100:
            placement_error(fmt, block_id, "width", "La position X et la largeur dépassent ensemble 100 %% du parent.")
        parent = effective_placement(parent_placement, fmt)
        limit = parent["height"] if parent["mode"] == "free" else 4096
        if rules["y"] + rules["height"] > limit:
            placement_error(fmt, block_id, "height", f"La position Y et la hauteur dépassent ensemble la limite de {limit} px.")


def patch_format(value, fmt, patch, clear, allowed):
    if fmt not in FORMATS:
        _invalid("format")
    _object(patch, "réglages", optional=allowed)
    if (not isinstance(clear, list) or len(clear) > len(allowed)
            or any(not isinstance(k, str) or k not in allowed or k in patch for k in clear)
            or len(set(clear)) != len(clear)):
        _invalid("héritage")
    previous = value.get(fmt, {})
    delta = {k: v for k, v in previous.items() if k not in clear}
    if allowed == PLACEMENT_FIELDS:
        old_mode = effective_placement(value, fmt)["mode"]
        base_mode = value.get("base", {}).get("mode", "flow") if fmt != "base" else "flow"
        new_mode = patch.get("mode", delta.get("mode", base_mode))
        if "mode" in patch and old_mode != new_mode:
            delta = {}
    delta.update(patch)
    if delta or fmt == "base":
        value[fmt] = delta
    else:
        value.pop(fmt, None)
