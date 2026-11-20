"""Reviewed Figma observations projected into the ordinary Studio composition."""
from collections import defaultdict
from copy import deepcopy
import json
from uuid import uuid4

from django.core.exceptions import ValidationError

from .catalogue import definitions_du_site
from .catalogue_v1 import PARAMETERS, manifest
from .validation import check_navigation_document


def refuse(message):
    raise ValidationError(message)


def renderers(node):
    kind, name = node["type"], node.get("name", "").casefold()
    if node.get("image"):
        return ["image"]
    if kind == "TEXT":
        heading = (node.get("font_size") or 0) >= 28 or name.startswith(("titre", "heading", "title"))
        return ["heading", "text", "signature"] if heading else ["text", "heading", "signature"]
    if kind == "INSTANCE" and ("button" in name or "bouton" in name):
        return ["button"]
    if kind in {"FRAME", "GROUP", "SECTION"}:
        return ["container"]
    return []


def observed_props(node, renderer):
    text = node.get("text") or ""
    if renderer == "container":
        base = {}
        gap = node.get("gap")
        if type(gap) is int and 0 <= gap <= 128:
            base["gap"] = gap
        return {"layout": {"base": base}}
    if renderer == "heading":
        return {"text": text, "level": 2}
    if renderer in {"text", "signature"}:
        return {"text": text}
    if renderer == "button":
        return {"label": text or node.get("name", ""), "url": ""}
    if renderer == "image":
        return {"alt": "", "media": {"kind": "media", "ref_id": ""}}
    return {}


def propose(site_id, observation):
    catalogue = [r for r in definitions_du_site(site_id) if not r["retired"] and r["renderer"] in PARAMETERS
                 and r["renderer"] != "article" and r["props"] == manifest(r["renderer"])["props"]]
    catalogue.sort(key=lambda r: (r["scope"], r["key"], r["version"]))
    rows = []
    review_bytes = 0
    seen = set()
    for frame in observation["frames"]:
        root = {**frame, "type": "FRAME", "parent_id": None}
        for node in [root, *frame["nodes"]]:
            if node["id"] in seen:
                refuse("Des frames sélectionnées se recouvrent. Choisissez des branches distinctes.")
            seen.add(node["id"])
            kinds = renderers(node)
            mapping = node.get("mapping")
            exact = next((r for r in catalogue if mapping and all(r[k] == mapping.get(k)
                         for k in ("scope", "key", "version"))), None)
            if exact:
                kinds = [exact["renderer"], *kinds]
            candidates = [r for r in catalogue if r["renderer"] in kinds]
            preferred = [r for r in candidates if r["renderer"] == kinds[0]] if kinds else []
            pick = exact or (preferred[0] if not mapping and len(preferred) == 1 and preferred[0]["scope"] == "global" else None)
            suggested_type = pick["renderer"] if pick else next(iter(kinds), "")
            reason = ("Clé de composant reliée au catalogue du site." if exact else
                      "Plusieurs définitions compatibles. Choisissez la version à retenir." if len(preferred) > 1 else
                      "Structure et propriétés compatibles avec le catalogue." if candidates else
                      "Composant interne à concevoir.")
            gaps = list(node.get("gaps") or [])
            if mapping and not exact:
                gaps.append("La correspondance configurée est indisponible dans le catalogue actuel.")
            if node.get("layout") == "HORIZONTAL":
                gaps.append("Disposition horizontale à adapter dans le canvas.")
            if suggested_type == "image":
                gaps.append("Choisissez un média du site réutilisable et son texte alternatif.")
            if suggested_type == "button":
                gaps.append("Vérifiez le libellé et renseignez une destination HTTPS.")
            variants = {str(v).casefold() for v in (node.get("variant") or {}).values()}
            variant = next((v for v in ("primary", "secondary") if v in variants and suggested_type == "button"), "")
            if variants and not variant:
                gaps.append("Variante fournisseur sans équivalent direct.")
            rows.append(dict(id=node["id"], frame_id=frame["id"], parent_id=node.get("parent_id"),
                             name=node["name"], type=node["type"], text=node.get("text") or "", reason=reason,
                             gaps=gaps, observed=node.get("observed") or {}, variant=variant,
                             candidates=[{k:r[k] for k in ("id","scope","key","version","label","renderer")} for r in candidates],
                             suggested=pick["id"] if pick else "", props=observed_props(node, suggested_type),
                             tokens=dict(node.get("tokens") or {})))
            review_bytes += len(json.dumps(rows[-1], ensure_ascii=False).encode())
            if len(rows) > 2000 or review_bytes > 4 * 1024 * 1024:
                refuse("La revue est trop volumineuse. Sélectionnez moins de frames.")
    return rows


def resolve_block(row, decision):
    if not isinstance(decision, dict) or decision.get("action") not in ("accept", "correct", "exclude"):
        refuse("Décidez du sort de chaque élément avant la confirmation.")
    if decision["action"] == "exclude":
        return None
    target = decision.get("definition") or row["suggested"]
    candidate = next((c for c in row["candidates"] if c["id"] == target), None)
    if candidate is None:
        refuse("Choisissez une définition compatible ou écartez cet élément.")
    props = decision.get("props", row["props"])
    tokens = decision.get("tokens", row["tokens"])
    variant = decision.get("variant", row["variant"])
    if not isinstance(props, dict) or not isinstance(tokens, dict) or not isinstance(variant, str):
        refuse("Les propriétés ou l’apparence de cet élément sont invalides.")
    node = dict(id=str(uuid4()), children=[], props=deepcopy(props),
                definition={k:candidate[k] for k in ("scope","key","version")})
    if candidate["renderer"] == "container" and "gap" in row["tokens"]:
        layout = node["props"].get("layout")
        if not isinstance(layout, dict) or not isinstance(layout.get("base"), dict):
            refuse("La disposition du conteneur est invalide.")
        if "gap" in tokens:
            layout["base"]["gap"] = tokens["gap"]
        else:
            layout["base"].pop("gap", None)
    appearance = {}
    if tokens:
        appearance["tokens"] = dict(tokens)
    if variant:
        appearance["variant"] = variant
    if appearance:
        node["appearance"] = appearance
    return node


def hierarchy(rows, decisions):
    blocks, locations = {}, {}
    siblings = defaultdict(int)
    for row in rows:
        key, parent = row["id"], row["parent_id"]
        block = resolve_block(row, decisions.get(key))
        if parent and parent not in blocks:
            refuse("La hiérarchie de la frame est incomplète.")
        if block is not None and parent and blocks[parent] is None:
            refuse("Écartez aussi les enfants de la branche exclue.")
        blocks[key] = block
        if block is None:
            continue
        if parent:
            blocks[parent]["children"].append(block)
            address = (*locations[parent], row["name"])
        else:
            address = ()
        locations[key] = address
        siblings[address] += 1
    return blocks, locations, siblings


def merge_format(base, alternate, fmt, trace):
    by_path = {address:base[0][key] for key,address in base[1].items()}
    for key, address in alternate[1].items():
        target = by_path.get(address)
        source = alternate[0][key]
        if target is None or base[2][address] != 1 or alternate[2][address] != 1:
            refuse("Une occurrence de la variante est absente ou ambiguë dans la base. Écartez-la ou séparez les pages.")
        if target["definition"] != source["definition"]:
            refuse("Les variantes associées doivent retenir la même définition.")
        props = source["props"]
        original = target["props"]
        if "layout" in props and "layout" in original:
            new_layout = props["layout"].get("base", {})
            if new_layout != original["layout"]["base"]:
                original["layout"][fmt] = deepcopy(new_layout)
        elif props != original:
            refuse("Les contenus diffèrent selon le format. Corrigez-les, écartez la variante ou séparez les pages.")
        a, b = deepcopy(source.get("appearance", {})), deepcopy(target.get("appearance", {}))
        if 'layout' in props:
            # Container spacing can vary by viewport through its canonical layout.
            for appearance in (a, b):
                if "tokens" in appearance:
                    appearance["tokens"].pop("gap", None)
                    if not appearance["tokens"]:
                        del appearance["tokens"]
        if a != b:
            refuse("Le modèle conserve une apparence commune. Corrigez ou écartez les valeurs divergentes.")
        trace[key] = target["id"]


def project(site_id, observation, proposals, decisions, destinations, existing):
    if not isinstance(decisions, dict) or set(decisions) != {r["id"] for r in proposals}:
        refuse("Chaque élément de l’analyse exige une décision explicite.")
    frames = {f["id"] for f in observation["frames"]}
    if (not isinstance(destinations, list) or len(destinations) != len(frames)
            or any(not isinstance(d,dict) for d in destinations)
            or {d.get("frame_id") for d in destinations} != frames):
        refuse("Attribuez une destination à chaque frame sélectionnée.")
    groups = defaultdict(list)
    for d in destinations:
        if (not isinstance(d.get("group"), str) or not d["group"].strip() or len(d["group"]) > 120
                or d.get("format") not in ("desktop","tablet","mobile") or type(d.get("base")) is not bool):
            refuse("Précisez le groupe, le rôle de base et le format de chaque frame.")
        groups[d["group"]].append(d)
    if existing and existing.get("schema_version") not in (1,2,3,4):
        refuse("Le schéma de la révision existante est incompatible.")
    doc = deepcopy(existing) if existing else {"pages":[],"menus":[],"theme":{}}
    doc["schema_version"] = 4
    old_pages = {p["id"] for p in doc["pages"]}
    root = next((p["id"] for p in doc["pages"] if p["parent_id"] is None), None)
    homes = [d for d in destinations if d.get("home") and d["base"]]
    if not existing and len(homes) != 1:
        refuse("Choisissez une seule page d’accueil parmi les frames de base.")
    page_ids = {group:str(uuid4()) for group in groups}
    if not existing:
        root = page_ids[homes[0]["group"]]
    by_frame = defaultdict(list)
    for row in proposals:
        by_frame[row["frame_id"]].append(row)
    used_paths = {(p["parent_id"], p["slug"]) for p in doc["pages"]}
    trace = {}
    for group, members in groups.items():
        bases = [d for d in members if d["base"]]
        if len(bases) != 1 or len({d["format"] for d in members}) != len(members):
            refuse("Chaque page requiert une seule base et au plus une frame par format.")
        base = bases[0]
        key = base["frame_id"]
        tree = hierarchy(by_frame[key], decisions)
        first = tree[0][key]
        if first is None:
            refuse("Conservez le conteneur de la frame de base ou recommencez avec une sélection plus petite.")
        trace.update({k:v["id"] for k,v in tree[0].items() if v is not None})
        for alt in members:
            if alt is base:
                continue
            other = hierarchy(by_frame[alt["frame_id"]], decisions)
            if alt["format"] == "desktop":
                refuse("Pour regrouper une frame bureau avec d’autres formats, choisissez-la comme base.")
            merge_format(tree, other, alt["format"], trace)
        page_id = page_ids[group]
        parent = base.get("parent_id") or root
        if parent != root and parent not in old_pages:
            refuse("Le parent de destination doit appartenir au brouillon du site.")
        page = dict(id=page_id, title=base.get("title"), slug="" if page_id==root else base.get("slug"),
                    parent_id=None if page_id==root else parent,
                    sections=[dict(id=str(uuid4()), layout={"base":{}}, blocks=[first])])
        path = (page["parent_id"], page["slug"])
        if path in used_paths:
            refuse("Ce segment est déjà utilisé sous la page parente. Modifiez le segment dans Pages et formats.")
        used_paths.add(path)
        doc["pages"].append(page)
        for d in members:
            frame = d["frame_id"]
            if frame in trace:
                trace[frame+"@container"] = trace[frame]
            trace[frame] = page_id
    return check_navigation_document(doc, site_id, existing or {"pages":[],"theme":{}}), trace
