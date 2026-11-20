"""Règles du document V3 et résolution des références dans le site courant."""

from functools import lru_cache
import json
import re

from django.core.exceptions import ValidationError

from . import catalogue
from .catalogue_v1 import PARAMETERS
from .validation import _array, _external_url, _integer, _invalid, _layout, _object, _text, _uuid

COLORS = ("accent", "background", "ink")
DEFAULTS = {"accent": "#304860", "background": "#FFFFFF", "ink": "#202020", "gap": 0, "font": "system"}


def block_lists(document):
    """Walk a stored tree with the owning page and sibling list, in display order."""

    def walk(page, siblings):
        for block in siblings:
            yield page, siblings, block
            yield from walk(page, block["children"])

    for page in document["pages"]:
        for section in page["sections"]:
            yield from walk(page, section["blocks"])


def definition_key(ref):
    return ref["scope"], ref["key"], ref["version"]


def checked_key(ref, path):
    _object(ref, path, ("scope", "key", "version"))
    if ref["scope"] not in ("global", "site"):
        _invalid(path)
    _text(ref["key"], path, 120)
    _integer(ref["version"], path, 1)
    return definition_key(ref)


def token_values(tokens, permitted, path):
    _object(tokens, path, optional=permitted)
    for name, value in tokens.items():
        if name in COLORS:
            if not isinstance(value, str) or not re.fullmatch(r"#[a-fA-F0-9]{6}", value):
                _invalid(path + "." + name)
        elif name == "gap":
            _integer(value, path + ".gap", 0, 128)
        elif name == "font":
            if value not in ("system", "dm-sans"):
                _invalid(path + ".font")
        else:
            _invalid(path)


def effective_appearance(theme, block, manifest):
    setting = next((s for s in theme.get("components", ()) if s["definition"] == block["definition"]), {})
    specific = block.get("appearance", {})
    values = {**DEFAULTS, **theme, **setting.get("tokens", {}), **specific.get("tokens", {})}
    return {
        "variant": specific.get("variant", setting.get("variant", manifest["variants"][0])),
        "tokens": {key: values[key] for key in manifest["tokens"] if key in values},
    }


def same_json(a, b):
    # Python equality conflates False with 0 and True with 1; JSON contract types do not.
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


class AppearanceContract:
    def __init__(self, site_id, previous=None, preserve=False):
        self.manifests = {definition_key(m): m for m in catalogue.definitions_du_site(site_id)}
        self.reference = lru_cache(maxsize=2000)(
            lambda kind, ref: catalogue.reference(site_id, kind, ref)
        )
        self.previous = previous or {"pages": [], "theme": {}}
        self.old_blocks = {(p["id"], b["id"]): b for p, _, b in block_lists(self.previous)}
        self.preserve = preserve

    def manifest(self, ref, path, already_pinned):
        key = checked_key(ref, path)
        manifest = self.manifests.get(key)
        if not manifest or (manifest["retired"] and not already_pinned):
            raise ValidationError(
                "Version du composant indisponible pour ce site.", code="component_unavailable"
            )
        if (
            manifest["renderer"] not in PARAMETERS
            or manifest["props"] != PARAMETERS[manifest["renderer"]]
        ):
            raise ValidationError(
                "Le rendu de cette version est incompatible.", code="renderer_incompatible"
            )
        return manifest

    def media(self, value, kind, path):
        _object(value, path, ("kind", "ref_id"))
        _uuid(value["ref_id"], path)
        if value["kind"] != kind or not self.reference(kind, value["ref_id"]):
            raise ValidationError("Ressource indisponible pour ce site.", code="resource_unavailable")

    def appearance(self, value, manifest, path):
        _object(value, path, optional=("variant", "tokens"))
        if "variant" in value and value["variant"] not in manifest["variants"]:
            _invalid(path + ".variant")
        if "tokens" in value:
            token_values(value["tokens"], manifest["tokens"], path + ".tokens")

    def block(self, page_id, block, path):
        previous = self.old_blocks.get((page_id, block["id"]))
        # Only the service that builds a candidate from the locked head enables this.
        if (
            self.preserve
            and previous
            and all(
                same_json(previous.get(k), block.get(k)) for k in ("definition", "props", "appearance")
            )
            and (previous["children"] or not block["children"])
        ):
            return
        manifest = self.manifest(
            block["definition"],
            path + ".definition",
            previous and previous["definition"] == block["definition"],
        )
        self.appearance(block.get("appearance", {}), manifest, path + ".appearance")
        if block["children"] and manifest["renderer"] != "container":
            _invalid(path + ".children")
        props, schema = block["props"], manifest["props"]
        _object(props, path + ".props", schema.keys())
        for name, kind in schema.items():
            value, field = props[name], path + ".props." + name
            if kind in ("text", "label", "alt"):
                _text(value, field, {"text": 4000, "label": 120, "alt": 300}[kind])
            elif kind == "level":
                _integer(value, field, 1, 6)
            elif kind == "https":
                _external_url(value, field)
            elif kind == "layout":
                _layout(value, field)
            elif kind in ("media", "wagtail_content"):
                self.media(value, kind, field)
            else:
                _invalid(field)

    def preference(self, value, path):
        _object(value, path, ("definition",), ("variant", "tokens"))
        key = checked_key(value["definition"], path + ".definition")
        old = next(
            (
                p
                for p in self.previous["theme"].get("components", ())
                if p["definition"] == value["definition"]
            ),
            None,
        )
        if not (self.preserve and same_json(value, old)):
            manifest = self.manifest(value["definition"], path + ".definition", old is not None)
            self.appearance({k: v for k, v in value.items() if k != "definition"}, manifest, path)
        return key

    def theme(self, theme):
        _object(theme, "theme", optional=(*DEFAULTS, "media", "components"))
        token_values({k: v for k, v in theme.items() if k in DEFAULTS}, DEFAULTS, "theme")
        if "media" in theme and not (
            self.preserve
            and "media" in self.previous["theme"]
            and same_json(theme["media"], self.previous["theme"]["media"])
        ):
            self.media(theme["media"], "media", "theme.media")
        components = _array(theme.get("components", []), "theme.components")
        if len(components) > 100:
            _invalid("theme.components")
        seen = set()
        for index, pref in enumerate(components):
            key = self.preference(pref, f"theme.components[{index}]")
            if key in seen:
                _invalid("theme.components")
            seen.add(key)
