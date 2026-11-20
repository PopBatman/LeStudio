"""Validation of the versioned Studio composition document."""
import json
import re
from copy import deepcopy
from urllib.parse import urlsplit
from uuid import UUID, uuid4

from django.core.exceptions import ValidationError


MAX_BYTES = 1_048_576
MAX_RAW_BYTES = 4 * MAX_BYTES
MAX_NODES = 2_000
MAX_DEPTH = 12
SUPPORTED_VERSIONS = (1, 2, 3, 4)
MAX_MENUS = 20
MAX_MENU_ITEMS = 500
MAX_MENU_DEPTH = 6
SCREENS = ("desktop", "tablet", "mobile")
DNS_LABEL = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?")


def _invalid(path):
    # Paths contain only known field names and numeric indices, never supplied content.
    raise ValidationError(f"Valeur de composition invalide : {path}.", code="invalid_document")


def _object(value, path, required=(), optional=()):
    if not isinstance(value, dict) or not set(required).issubset(value):
        _invalid(path)
    if value.keys() - set(required) - set(optional):
        _invalid(path)


def _array(value, path):
    if not isinstance(value, list):
        _invalid(path)
    return value


def _integer(value, path, minimum, maximum=None):
    if type(value) is not int or value < minimum or (maximum is not None and value > maximum):
        _invalid(path)


def _text(value, path, limit):
    if not isinstance(value, str) or not value.strip() or len(value) > limit or "\0" in value:
        _invalid(path)


def _uuid(value, path):
    if not isinstance(value, str) or len(value) != 36:
        _invalid(path)
    try:
        canonical = str(UUID(value))
    except ValueError:
        _invalid(path)
    if value != canonical:
        _invalid(path)


def _external_url(value, path):
    _text(value, path, 2048)
    if any(c.isspace() or ord(c) < 32 or 127 <= ord(c) <= 159 or c == "\\" for c in value):
        _invalid(path)
    try:
        url = urlsplit(value)
        port = url.port
    except ValueError:
        _invalid(path)
    if (url.scheme != "https" or not url.netloc.isascii() or not url.hostname
            or url.username is not None or "[" in url.netloc or url.netloc.endswith(":") or port == 0):
        _invalid(path)
    host = url.hostname.removesuffix(".")
    if len(host) > 253 or not all(DNS_LABEL.fullmatch(label) for label in host.split(".")):
        _invalid(path)


def _check_parents(items, path, max_depth):
    parents = {item["id"]: item["parent_id"] for item in items}
    for index, item in enumerate(items):
        ancestor = item["id"]
        for _ in range(max_depth):
            if ancestor not in parents:
                _invalid(f"{path}[{index}].parent_id")
            ancestor = parents[ancestor]
            if ancestor is None:
                break
        else:
            _invalid(f"{path}[{index}].parent_id")


def _menu_target(target, path, page_ids):
    _object(target, path, ("kind",), ("page_id", "url"))
    kind = target["kind"]
    if kind == "group":
        _object(target, path, ("kind",))
    elif kind == "page":
        _object(target, path, ("kind", "page_id"))
        _uuid(target["page_id"], path + ".page_id")
        if target["page_id"] not in page_ids:
            _invalid(path + ".page_id")
    elif kind == "external":
        _object(target, path, ("kind", "url"))
        _external_url(target["url"], path + ".url")
    else:
        _invalid(path + ".kind")


def _layout(value, path):
    _object(value, path, ("base",), ("tablet", "mobile"))
    for screen, rules in value.items():
        key = f"{path}.{screen}"
        _object(rules, key, optional=("gap", "display", "columns"))
        if "gap" in rules:
            _integer(rules["gap"], key + ".gap", 0, 128)
        if "columns" in rules:
            _integer(rules["columns"], key + ".columns", 1, 12)
        if "display" in rules and rules["display"] not in ("stack", "grid"):
            _invalid(key + ".display")
    for screen, rules in value.items():
        effective = {**value["base"], **rules}
        if effective.get("display", "stack") == "stack" and effective.get("columns", 1) != 1:
            _invalid(f"{path}.{screen}.columns")


class _Document:
    def __init__(self, site_id, resolve_definition, resolve_reference, preserved_blocks, appearance=None, canvas=False):
        self.canvas = canvas
        self.appearance = appearance
        self.site = site_id
        self.definition = resolve_definition
        self.reference = resolve_reference
        self.preserved_blocks = preserved_blocks
        self.ids = set()
        self.nodes = 0

    def identity(self, value, path):
        _uuid(value, path)
        if value in self.ids:
            _invalid(path)
        self.ids.add(value)

    def node(self, item, path, fields, optional=()):
        self.nodes += 1
        if self.nodes > MAX_NODES:
            _invalid(path)
        _object(item, path, fields, optional)
        self.identity(item["id"], path + ".id")

    def block(self, item, path, depth, page_id, layout=None, parent_placement=None):
        if depth > MAX_DEPTH:
            _invalid(path)
        optional = ("appearance", "placement") if self.canvas else ("appearance",) if self.appearance else ()
        self.node(item, path, ("id", "definition", "props", "children"), optional)
        if self.canvas and "placement" in item:
            from .placement import validate_placement
            validate_placement(item["placement"], layout or {}, parent_placement or {}, path + ".placement", item["id"])
        if self.appearance:
            children = _array(item["children"], path+".children")
            self.appearance.block(page_id, item, path)
            child_layout = item["props"].get("layout", {}) if children else {}
            # Historic components may use a text property named layout.
            if not isinstance(child_layout, dict):
                child_layout = {}
            for index, child in enumerate(children):
                self.block(child, f"{path}.children[{index}]", depth+1, page_id,
                           child_layout, item.get("placement"))
            return
        definition = item["definition"]
        _object(definition, path + ".definition", ("scope", "key", "version"))
        scope, key, version = definition["scope"], definition["key"], definition["version"]
        if scope not in ("site", "global"):
            _invalid(path + ".definition.scope")
        _text(key, path + ".definition.key", 120)
        _integer(version, path + ".definition.version", 1)
        children = _array(item["children"], path + ".children")
        props, field = item["props"], path + ".props"

        if (scope, key, version) == ("global", "container", 1):
            _object(props, field, ("layout",))
            _layout(props["layout"], field + ".layout")
            for index, child in enumerate(children):
                self.block(child, f"{path}.children[{index}]", depth + 1, page_id)
            return

        if children:
            _invalid(path + ".children")
        if scope == "global" and version == 1 and key in ("text", "heading"):
            _object(props, field, ("text", "level") if key == "heading" else ("text",))
            _text(props["text"], field + ".text", 4000)
            if key == "heading":
                _integer(props["level"], field + ".level", 1, 6)
            return

        # Navigation commands can carry an unchanged stored leaf without opening its resource.
        if self.preserved_blocks.get(item["id"]) == item:
            return
        schema = self.definition(self.site, scope, key, version) if self.definition else None
        if not isinstance(schema, dict):
            _invalid(path + ".definition")
        _object(props, field, schema.keys())
        for name, kind in schema.items():
            value, prop_path = props[name], f"{field}.{name}"
            if kind == "text":
                _text(value, prop_path, 4000)
                continue
            if kind not in ("media", "wagtail_content"):
                _invalid(field)
            _object(value, prop_path, ("kind", "ref_id"))
            _uuid(value["ref_id"], prop_path + ".ref_id")
            if (value["kind"] != kind or self.reference is None
                    or self.reference(self.site, kind, value["ref_id"]) is not True):
                _invalid(prop_path)

    def pages(self, pages):
        if not 1 <= len(_array(pages, "pages")) <= 100:
            _invalid("pages")
        slugs = set()
        for index, page in enumerate(pages):
            path = f"pages[{index}]"
            _object(page, path, ("id", "parent_id", "slug", "title", "sections"))
            self.identity(page["id"], path + ".id")
            parent, slug = page["parent_id"], page["slug"]
            if parent is None:
                if slug != "":
                    _invalid(path + ".slug")
            else:
                _uuid(parent, path + ".parent_id")
                if not isinstance(slug, str) or len(slug) > 80 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
                    _invalid(path + ".slug")
            if (parent, slug) in slugs:
                _invalid(path + ".slug")
            slugs.add((parent, slug))
            _text(page["title"], path + ".title", 120)
            for number, section in enumerate(_array(page["sections"], path + ".sections")):
                field = f"{path}.sections[{number}]"
                self.node(section, field, ("id", "layout", "blocks"))
                _layout(section["layout"], field + ".layout")
                for pos, block in enumerate(_array(section["blocks"], field + ".blocks")):
                    self.block(block, f"{field}.blocks[{pos}]", 1, page["id"], section["layout"])
        if not any(page["parent_id"] is None for page in pages):
            _invalid("pages")
        _check_parents(pages, "pages", MAX_DEPTH)

    def menus(self, menus, page_ids):
        if len(_array(menus, "menus")) > MAX_MENUS:
            _invalid("menus")
        count = 0
        for index, menu in enumerate(menus):
            path = f"menus[{index}]"
            _object(menu, path, ("id", "label", "items"))
            self.identity(menu["id"], path + ".id")
            _text(menu["label"], path + ".label", 120)
            items = _array(menu["items"], path + ".items")
            count += len(items)
            if count > MAX_MENU_ITEMS:
                _invalid(path + ".items")
            for number, item in enumerate(items):
                field = f"{path}.items[{number}]"
                _object(item, field, ("id", "parent_id", "label", "target", "visibility"))
                self.identity(item["id"], field + ".id")
                if item["parent_id"] is not None:
                    _uuid(item["parent_id"], field + ".parent_id")
                _text(item["label"], field + ".label", 120)
                _menu_target(item["target"], field + ".target", page_ids)
                screens = _array(item["visibility"], field + ".visibility")
                if (not 1 <= len(screens) <= len(SCREENS)
                        or any(screen not in SCREENS for screen in screens)
                        or len(set(screens)) != len(screens)):
                    _invalid(field + ".visibility")
            _check_parents(items, path + ".items", MAX_MENU_DEPTH)


def _unique_object(pairs):
    obj = dict(pairs)
    if len(obj) != len(pairs):
        _invalid("document")
    return obj


def _compact_size(value, remaining, depth=0):
    """Measure compact UTF-8 JSON incrementally, before consulting scoped providers."""
    if remaining <= 0 or depth > 64:  # V1 permits at most 12 nested blocks.
        _invalid("document")
    if isinstance(value, (dict, list)):
        # Brackets/braces, commas, and (for objects) one colon per key.
        size = 2 + max(0, len(value) - 1)
        if isinstance(value, dict):
            size += len(value)
            for key, item in value.items():
                if not isinstance(key, str):
                    _invalid("document")
                size += _compact_size(key, remaining - size, depth + 1)
                size += _compact_size(item, remaining - size, depth + 1)
        else:
            for item in value:
                size += _compact_size(item, remaining - size, depth + 1)
    else:
        if isinstance(value, str) and len(value) + 2 > remaining:
            _invalid("document")
        if value is not None and type(value) not in (str, bool, int, float):
            _invalid("document")
        scalar = json.dumps(value, ensure_ascii=False, allow_nan=False)
        size = len(scalar.encode("utf-8"))
    if size > remaining:
        _invalid("document")
    return size


def check_document(document, site_id, *, resolve_definition=None, resolve_reference=None):
    """Return a detached snapshot. Trusted resolvers receive only local scoped references."""
    return _check_document(document, site_id, resolve_definition, resolve_reference, {})


def check_navigation_document(document, site_id, previous, *, resolve_definition=None, resolve_reference=None):
    """Keep opaque blocks from this site's locked revision when no catalogue is available."""
    preserved = {}
    if resolve_definition is None and resolve_reference is None:
        sections = {page["id"]: page["sections"] for page in previous["pages"]}
        for page in document["pages"]:
            if page["sections"] != sections.get(page["id"]):
                continue
            for section in page["sections"]:
                pending = list(section["blocks"])
                while pending:
                    block = pending.pop()
                    preserved[block["id"]] = block
                    pending.extend(block["children"])
    return _check_document(document, site_id, resolve_definition, resolve_reference, preserved, previous, preserve=True)


def _check_document(document, site_id, resolve_definition, resolve_reference, preserved_blocks, previous=None, preserve=False):
    if isinstance(document, (str, bytes)):
        try:
            if len(document) > MAX_RAW_BYTES:
                _invalid("document")
            if isinstance(document, str) and len(document.encode("utf-8")) > MAX_RAW_BYTES:
                _invalid("document")
            raw = document.decode("utf-8") if isinstance(document, bytes) else document
            document = json.loads(raw, object_pairs_hook=_unique_object,
                                  parse_constant=lambda _: _invalid("document"))
        except (ValueError, RecursionError):
            _invalid("document")
    if not isinstance(document, dict) or type(document.get("schema_version")) is not int:
        _invalid("schema_version")
    if document["schema_version"] not in SUPPORTED_VERSIONS:
        raise ValidationError("Version du schéma de composition incompatible.", code="incompatible_schema")
    try:
        _compact_size(document, MAX_BYTES)
    except (ValueError, RecursionError):
        _invalid("document")
    _object(document, "document", ("schema_version", "pages", "menus", "theme"))
    if document["schema_version"] == 1 and document["menus"] != []:
        _invalid("menus")
    theme = document["theme"]
    appearance = None
    if document["schema_version"] >= 3:
        from .appearance_contract import AppearanceContract
        appearance = AppearanceContract(site_id, previous, preserve)
        appearance.theme(theme)
    else:
        _object(theme, "theme", optional=("accent", "gap"))
        if "accent" in theme and (not isinstance(theme["accent"], str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", theme["accent"])):
            _invalid("theme.accent")
        if "gap" in theme:
            _integer(theme["gap"], "theme.gap", 0, 128)

    validator = _Document(site_id, resolve_definition, resolve_reference, preserved_blocks, appearance, document["schema_version"] == 4)
    validator.pages(document["pages"])
    if document["schema_version"] >= 2:
        validator.menus(document["menus"], {page["id"] for page in document["pages"]})
    checked = json.loads(json.dumps(document, ensure_ascii=False, separators=(",", ":")))
    if document["schema_version"] == 4:
        from .appearance_contract import block_lists
        for _, _, block in block_lists(checked):
            placement = block.get("placement")
            if placement is None:
                continue
            for fmt in ("tablet", "mobile"):
                if placement.get(fmt) == {}:
                    del placement[fmt]
            if placement == {"base": {}}:
                del block["placement"]
    return checked


def remap_occurrence_ids(document, occurrence_map=None):
    """Copy a validated external document with fresh local IDs, preserving opaque resource IDs."""
    copy = deepcopy(document)
    pages = copy["pages"]
    page_ids = {page["id"]: str(uuid4()) for page in pages}
    if occurrence_map is not None:
        occurrence_map.update(page_ids)
    for page in pages:
        page["id"] = page_ids[page["id"]]
        if page["parent_id"] is not None:
            page["parent_id"] = page_ids[page["parent_id"]]
        for section in page["sections"]:
            section["id"] = str(uuid4())
            remaining = list(section["blocks"])
            while remaining:
                block = remaining.pop()
                old_id, block["id"] = block["id"], str(uuid4())
                if occurrence_map is not None:
                    occurrence_map[old_id] = block["id"]
                remaining.extend(block["children"])
    for menu in copy["menus"]:
        menu["id"] = str(uuid4())
        item_ids = {item["id"]: str(uuid4()) for item in menu["items"]}
        for item in menu["items"]:
            item["id"] = item_ids[item["id"]]
            if item["parent_id"] is not None:
                item["parent_id"] = item_ids[item["parent_id"]]
            if item["target"]["kind"] == "page":
                item["target"]["page_id"] = page_ids[item["target"]["page_id"]]
    return copy
