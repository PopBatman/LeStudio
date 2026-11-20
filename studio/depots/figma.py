"""Lecture bornée d'un fichier Figma explicitement attribué à un site."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import http.client
import json
import math
import os
from pathlib import Path
import re
import socket
from threading import Timer
from time import monotonic
from urllib.parse import urlencode
from uuid import UUID


MAX_BYTES = 8 * 1024 * 1024
MAX_NODES = 2000
MAX_FRAMES = 8
FRAME_TYPES = {"FRAME", "COMPONENT", "COMPONENT_SET"}
SITE_LINK = re.compile(r"https://www\.figma\.com/design/([A-Za-z0-9]+)(?:\?node-id=(\d+)-(\d+))?")
NODE_ID = re.compile(r"[0-9]+:[0-9]+")
LAYER_ID = re.compile(r"[0-9I:;.-]{1,256}")


class FigmaError(Exception):
    messages = {
        "profile": "Le profil de lecture Figma du site doit être configuré.",
        "inaccessible": "Cette source Figma est absente ou inaccessible pour ce site.",
        "changed": "La version du fichier a changé. Relancez l’analyse.",
        "limited": "Figma a temporairement limité la lecture. Réessayez après le délai indiqué.",
        "unavailable": "Figma ne répond pas actuellement. Relancez la lecture ultérieurement.",
        "incomplete": "L’analyse est incomplète. Vérifiez ou réduisez la sélection de frames.",
    }

    def __init__(self, code, retry_after=None):
        self.code = code
        self.retry_after = retry_after
        super().__init__(self.messages[code])


@dataclass(frozen=True, repr=False)
class Profile:
    file_key: str
    node_id: str | None
    generation: str
    token: str = field(repr=False)
    components: dict = field(default_factory=dict)


def _file(path, maximum):
    if not isinstance(path, str) or not Path(path).is_absolute():
        raise ValueError
    with open(path, "rb") as source:
        data = source.read(maximum + 1)
    if len(data) > maximum:
        raise ValueError
    return data


def load_profile(site_id, figma_url):
    link = SITE_LINK.fullmatch(figma_url) if isinstance(figma_url, str) and len(figma_url) <= 2048 else None
    if not link:
        raise FigmaError("inaccessible")
    key, left, right = link.groups()
    try:
        site = str(UUID(str(site_id)))
        config = json.loads(_file(os.environ["STUDIO_FIGMA_PROFILES"], 262144))[site]
        if not isinstance(config, dict) or not isinstance(config["files"], list):
            raise ValueError
        if key not in config["files"]:
            raise FigmaError("inaccessible")
        if not isinstance(config["generation"], str) or not config["generation"].strip():
            raise ValueError
        token = _file(config["token_file"], 4096).decode("ascii").strip()
        if not re.fullmatch(r"[!-~]+", token):
            raise ValueError
        mappings = config.get("components", {})
        if not isinstance(mappings, dict):
            raise ValueError
        for source, ref in mappings.items():
            if (not 0 < len(source) <= 256 or not isinstance(ref, dict)
                    or set(ref) != {"scope","key","version"} or ref["scope"] not in ("site","global")
                    or not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", ref["key"])
                    or type(ref["version"]) is not int or ref["version"] < 1):
                raise ValueError
        configuration = json.dumps(config, sort_keys=True, separators=(",", ":")).encode()
        generation = sha256(site.encode() + b"\0" + configuration + b"\0" + token.encode()).hexdigest()
        return Profile(key, f"{left}:{right}" if left else None, generation, token, mappings)
    except (ValueError, TypeError, OSError, KeyError, RecursionError):
        raise FigmaError("profile") from None


@dataclass
class _Budget:
    deadline: float = field(default_factory=lambda: monotonic() + 30)
    remaining: int = MAX_BYTES
    nodes: int = 0

    def visit(self):
        self.nodes += 1
        if self.nodes > MAX_NODES or monotonic() >= self.deadline:
            raise FigmaError("incomplete")


def _get(profile, budget, endpoint, query):
    remaining = budget.deadline - monotonic()
    if remaining <= 0:
        raise FigmaError("unavailable")
    conn = http.client.HTTPSConnection("api.figma.com", timeout=min(10, remaining))
    timer = None
    try:
        conn.connect()
        # The peer can send data incrementally. An absolute deadline also covers slow headers and bodies.
        tls_socket = conn.sock
        def interrupt():
            try:
                tls_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        timer = Timer(max(0, budget.deadline - monotonic()), interrupt)
        timer.start()
        path = f"/v1/files/{profile.file_key}{endpoint}?{urlencode(query)}"
        conn.request("GET", path, headers={"X-Figma-Token":profile.token,"Accept":"application/json",
                                          "Accept-Encoding":"identity", "User-Agent":"LeStudio-Figma/1"})
        response = conn.getresponse()
        if response.status in (401, 403, 404):
            raise FigmaError("inaccessible")
        if response.status == 429:
            delay = response.getheader("Retry-After", "")
            raise FigmaError("limited", int(delay) if re.fullmatch(r"[0-9]{1,9}", delay) else 60)
        if response.status != 200:
            raise FigmaError("unavailable" if response.status >= 500 else "incomplete")
        if response.getheader("Content-Encoding", "identity").lower() != "identity":
            raise FigmaError("incomplete")
        if response.getheader("Content-Type", "").split(";")[0].lower() != "application/json":
            raise FigmaError("incomplete")
        length = response.getheader("Content-Length")
        if length and (not re.fullmatch(r"[0-9]{1,12}", length) or int(length) > budget.remaining):
            raise FigmaError("incomplete")
        data = response.read(budget.remaining + 1)
        budget.remaining -= len(data)
        if budget.remaining < 0 or (length and len(data) != int(length)):
            raise FigmaError("incomplete")
        result = json.loads(data)
        if not isinstance(result, dict):
            raise FigmaError("incomplete")
        return result
    except (OSError, http.client.HTTPException):
        raise FigmaError("unavailable") from None
    except (ValueError, RecursionError):
        raise FigmaError("incomplete") from None
    finally:
        if timer:
            timer.cancel()
        conn.close()


def _required_text(value, maximum=256):
    if not isinstance(value, str) or len(value) > maximum or "\0" in value:
        raise FigmaError("incomplete")
    value.encode("utf-8")  # PostgreSQL JSON cannot represent unpaired surrogates.
    return value


def _layer_id(node):
    value = _required_text(node["id"])
    if not LAYER_ID.fullmatch(value):
        raise FigmaError("incomplete")
    return value


def _frame_info(node, page):
    return {"id":_layer_id(node), "name":_required_text(node["name"]), "page":page}


def _children(node):
    children = node.get("children", [])
    if not isinstance(children, list):
        raise FigmaError("incomplete")
    return children


def _inventory(profile, budget):
    if profile.node_id:
        # Only this subtree enters the inventory, even when dependencies accompany the response.
        response = _get(profile, budget, "/nodes", {"ids":profile.node_id, "depth":3})
        item = response["nodes"].get(profile.node_id)
        if not item or item["document"]["id"] != profile.node_id:
            raise FigmaError("inaccessible")
        roots = [(item["document"], "Sélection de la remise")]
    else:
        response = _get(profile, budget, "", {"depth":3})
        root = response["document"]
        if root["type"] != "DOCUMENT":
            raise FigmaError("incomplete")
        roots = [(page, "") for page in _children(root)]
    frames = []
    pending = list(reversed(roots))
    while pending:
        node, page = pending.pop()
        budget.visit()
        if node["type"] in FRAME_TYPES:
            frame = _frame_info(node, page)
            if not NODE_ID.fullmatch(frame["id"]):
                raise FigmaError("incomplete")
            frames.append(frame)
        elif node["type"] in {"DOCUMENT", "CANVAS", "SECTION", "GROUP"}:
            if node["type"] == "CANVAS":
                page = _required_text(node["name"])
            pending.extend((child, page) for child in reversed(_children(node)))
    if len({f["id"] for f in frames}) != len(frames):
        raise FigmaError("incomplete")
    version = _required_text(response["version"], 128)
    if not version:
        raise FigmaError("incomplete")
    return {"frames":frames, "version":version, "observed_at":datetime.now(timezone.utc).isoformat()}


def inventory(profile):
    try:
        return _inventory(profile, _Budget())
    except (TypeError, KeyError, AttributeError, ValueError, RecursionError):
        raise FigmaError("incomplete") from None


def _number(value):
    return value if type(value) in (float, int) and -1e7 <= value <= 1e7 and math.isfinite(value) else None


def _styles(node):
    observed, tokens, gaps = {}, {}, []
    style = node.get("style", {})
    family, size = style.get("fontFamily"), _number(style.get("fontSize"))
    if family:
        observed["font"] = _required_text(family)
        if family.lower() in {"dm sans", "system", "system-ui"}:
            tokens["font"] = "dm-sans" if family.lower() == "dm sans" else "system"
        else:
            gaps.append("Police à adapter au catalogue Studio.")
    if size is not None:
        observed["font_size"] = size
        gaps.append("Taille typographique à comparer au rendu du composant.")
    gap = _number(node.get("itemSpacing"))
    if gap is not None:
        observed["spacing"] = gap
        if 0 <= gap <= 128 and int(gap) == gap:
            tokens["gap"] = int(gap)
        else:
            gaps.append("Espacement hors des valeurs admises.")
    fills = node.get("fills", [])
    if not isinstance(fills, list):
        raise FigmaError("incomplete")
    visible = [p for p in fills if p.get("visible",True)]
    image = any(p.get("type") == "IMAGE" for p in visible)
    if image:
        gaps.append("Choisir un média du site dont les droits sont vérifiés.")
    if len(visible) == 1 and visible[0].get("type") == "SOLID":
        paint = visible[0]
        rgb = [_number(paint["color"].get(k)) for k in "rgb"]
        if all(v is not None and 0 <= v <= 1 for v in rgb):
            color = "#" + "".join(f"{round(v*255):02X}" for v in rgb)
            observed["fill"] = color
            if paint.get("opacity",1)==1 and node.get("opacity",1)==1:
                tokens["ink" if node["type"]=="TEXT" else "background"] = color
            else:
                gaps.append("Opacité à adapter.")
        else:
            gaps.append("Couleur non représentable.")
    elif visible and not (image and len(visible)==1):
        gaps.append("Remplissages multiples ou dégradés à adapter.")
    if node.get("boundVariables"):
        gaps.append("Variable Figma liée, valeur nommée à vérifier.")
    if node.get("styles"):
        observed["styles"] = {k:_required_text(v) for k,v in node["styles"].items()
                              if k in {"fill","fills","text","stroke","effect","grid"}}
    return tokens, observed, gaps, image


def _layer(node, parent, components, profile):
    kind, name = _required_text(node["type"]), _required_text(node["name"])
    tokens, observed, gaps, image = _styles(node)
    box = node.get("absoluteBoundingBox") or {}
    meta = components.get(node.get("componentId"), {}) or {}
    key = _required_text(meta["key"]) if meta.get("key") else None
    variant = {}
    for prop, value in node.get("componentProperties", {}).items():
        if value.get("type") == "VARIANT":
            variant[_required_text(prop)] = _required_text(value["value"])
    return {"id":_layer_id(node),"parent_id":parent,"type":kind,"name":name,
            "text":_required_text(node.get("characters",""),4000),"component_key":key,
            "mapping":profile.components.get(key),"tokens":tokens,"observed":observed,
            "font_size":observed.get("font_size"),"image":image,"variant":variant,"gaps":gaps,
            "width":_number(box.get("width")),"height":_number(box.get("height")),
            "layout":_required_text(node.get("layoutMode","NONE")),"gap":observed.get("spacing")}


def _frame(source, item, profile, budget, seen):
    root = item["document"]
    if root["id"] != source["id"] or root["type"] not in FRAME_TYPES:
        raise FigmaError("inaccessible")
    components = item.get("components", {})
    frame = _layer(root, None, components, profile)
    frame.update(page=source["page"], nodes=[])
    hidden = 0
    pending = [(node,root["id"],1) for node in reversed(_children(root))]
    while pending:
        node, parent, depth = pending.pop()
        budget.visit()
        if depth > 32:
            raise FigmaError("incomplete")
        if node.get("visible", True) is False:
            hidden += 1
            continue
        layer = _layer(node, parent, components, profile)
        if layer["id"] in seen:
            raise FigmaError("incomplete")
        seen.add(layer["id"])
        frame["nodes"].append(layer)
        pending.extend((child,layer["id"],depth+1) for child in reversed(_children(node)))
    if hidden:
        frame["gaps"].append(f"Calques masqués exclus de la proposition : {hidden}.")
    return frame


def inspect_frames(profile, version, frame_ids):
    """Recheck the eligible inventory and read selected subtrees at its exact version."""
    try:
        if (not isinstance(frame_ids, (list,tuple)) or not 1 <= len(frame_ids) <= MAX_FRAMES
                or any(not isinstance(v,str) or not NODE_ID.fullmatch(v) for v in frame_ids)
                or len(set(frame_ids)) != len(frame_ids)):
            raise FigmaError("incomplete")
        budget = _Budget()
        current = _inventory(profile, budget)
        if current["version"] != version:
            raise FigmaError("changed")
        available = {f["id"]:f for f in current["frames"]}
        if not set(frame_ids) <= available.keys():
            raise FigmaError("inaccessible")
        frames, seen = [], set(frame_ids)
        for offset in range(0,len(frame_ids),2):
            group = frame_ids[offset:offset+2]
            response = _get(profile,budget,"/nodes",{"ids":",".join(group),"version":version})
            if response["version"] != version:
                raise FigmaError("changed")
            for key in group:
                item = response["nodes"].get(key)
                if not item:
                    raise FigmaError("inaccessible")
                frames.append(_frame(available[key],item,profile,budget,seen))
        return {"version":version, "observed_at":current["observed_at"], "frames":frames}
    except (TypeError, KeyError, AttributeError, ValueError, RecursionError):
        raise FigmaError("incomplete") from None
