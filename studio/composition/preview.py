"""Préparer en lecture seule le rendu d'une révision, sur son instance confirmée."""
from base64 import b64decode, b64encode
from hashlib import sha256
from html.parser import HTMLParser
import re

from django.core.exceptions import ValidationError
from django.db import DatabaseError

from django.http import Http404

from raccordement.models import SiteConnection
from raccordement.profiles import ProfileError, load_profile
from raccordement.transport import ProbeError, canonical_json, read_preview

from . import catalogue
from .appearance_contract import block_lists, definition_key
from .catalogue_v1 import PARAMETERS, manifest as renderer_manifest
from .models import EditorialReference, SiteMedia
from .services import lire_revision


class PreviewError(Exception):
    messages = {
        "inaccessible": "Cette révision, cette page ou une ressource est inaccessible.",
        "changed": "Une ressource a changé depuis son association à cette révision.",
        "identity": "Le raccordement a changé. Vérifiez l’instance associée au site.",
        "authentication": "Le moteur refuse l’accès à l’aperçu. Vérifiez ses autorisations.",
        "unlinked": "Le site doit disposer d’un raccordement vérifié.",
        "unavailable": "Le moteur est indisponible. Réessayez après rétablissement de la connexion.",
        "incompatible": "Le moteur, la version demandée ou le rendu reçu est incompatible.",
    }

    def __init__(self, code):
        self.code = code
        super().__init__(self.messages[code])


def _connection(site_id):
    link = SiteConnection.objects.filter(site_id=site_id, confirmed_at__isnull=False,
                                         diagnostic="connected").first()
    if not link:
        raise PreviewError("unlinked")
    try:
        profile = load_profile(link.confirmed_profile)
    except ProfileError:
        raise PreviewError("unlinked") from None
    if (profile.site_id != link.site_id or profile.instance_id != link.instance_id
            or not isinstance(link.versions, dict)
            or profile.image_digest != link.versions.get("image_digest")
            or profile.engine_version != link.versions.get("engine_version")):
        raise PreviewError("identity")
    return link.attempt_id, profile


def _media(user, site_id, ref_id):
    data = catalogue.media_png(user, site_id, ref_id)
    return {"sha256": sha256(data).hexdigest(), "data": b64encode(data).decode("ascii")}


def _dependencies(user, site_id, instance_id, page, theme):
    definitions, media, articles = {}, {}, {}
    block_ids = []
    if "media" in theme:
        ref_id = theme["media"]["ref_id"]
        media[ref_id] = _media(user, site_id, ref_id)
    for _, _, block in block_lists({"pages": [page]}):
        block_ids.append(block["id"])
        ref = block["definition"]
        key = definition_key(ref)
        if key not in definitions:
            row = catalogue.definition(site_id, *key)
            if not row or row["renderer"] not in PARAMETERS:
                raise PreviewError("incompatible")
            renderer = row["renderer"]
            if any(row.get(k) != v for k, v in renderer_manifest(renderer).items()):
                raise PreviewError("incompatible")
            definitions[key] = {**ref, "renderer": renderer}
        for value in block["props"].values():
            if not isinstance(value, dict) or "ref_id" not in value:
                continue
            ref_id = value["ref_id"]
            if value["kind"] == "media" and ref_id not in media:
                media[ref_id] = _media(user, site_id, ref_id)
            if value["kind"] == "wagtail_content" and ref_id not in articles:
                pin = EditorialReference.objects.filter(site_id=site_id, instance_id=instance_id,
                    pk=ref_id, content_type="article").first()
                if not pin:
                    raise PreviewError("inaccessible")
                articles[ref_id] = {"page_id": pin.page_number, "published_revision_id": pin.published_revision}
    return {"definitions": list(definitions.values()), "articles": articles, "media": media}, block_ids


class _RenderedPage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.images = set()
        self.styles = []
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        if tag == "style":
            self.in_style = True
        attributes = dict(attrs)
        if (tag in {"script", "iframe", "object", "embed", "form", "base", "link", "svg", "math"}
                or len(attrs) != len(attributes) or "http-equiv" in attributes
                or any(name.startswith("on") or name in {"href", "srcset", "style"} for name in attributes)):
            raise PreviewError("incompatible")
        if "src" in attributes:
            if tag != "img" or not isinstance(attributes["src"], str):
                raise PreviewError("incompatible")
            self.images.add(attributes["src"])
        if "data-studio-block-id" in attributes:
            self.ids.append(attributes["data-studio-block-id"])

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False

    def handle_data(self, data):
        if self.in_style:
            self.styles.append(data)


def _verify_result(profile, result, payload, block_ids):
    if not isinstance(result, dict) or set(result) != {"html", "manifest"}:
        raise PreviewError("incompatible")
    html, manifest = result["html"], result["manifest"]
    if not isinstance(html, str) or not html.strip() or not isinstance(manifest, dict):
        raise PreviewError("incompatible")
    expected = {k: payload[k] for k in ("site_id", "instance_id", "revision_id", "revision_number",
                                         "page_id", "articles", "definitions")}
    expected.update(engine_version=profile.engine_version, image_digest=profile.image_digest,
                    sha256=sha256(canonical_json(payload)).hexdigest(), block_ids=block_ids,
                    html_sha256=sha256(html.encode("utf-8")).hexdigest(),
                    media={k: v["sha256"] for k, v in payload["media"].items()})
    if any(canonical_json(manifest.get(k)) != canonical_json(v) for k, v in expected.items()):
        raise PreviewError("incompatible")
    if (not isinstance(manifest.get("fonts"), dict) or
            not all(isinstance(h, str) and re.fullmatch("[0-9a-f]{64}", h) for h in (
                manifest.get("renderer_sha256"), manifest.get("css_sha256"), *manifest["fonts"].values()))):
        raise PreviewError("incompatible")
    parser = _RenderedPage()
    parser.feed(html)
    parser.close()
    css = "".join(parser.styles)
    images = {"data:image/png;base64," + m["data"] for m in payload["media"].values()}
    font_assets = re.findall(r"url\(data:font/woff2;base64,([A-Za-z0-9+/=]+)\)", css)
    font_hashes = {sha256(b64decode(asset, validate=True)).hexdigest() for asset in font_assets}
    if (parser.ids != block_ids or len(set(block_ids)) != len(block_ids)
            or parser.images != images or sha256(css.encode()).hexdigest() != manifest["css_sha256"]
            or font_hashes != set(manifest["fonts"].values())):
        raise PreviewError("incompatible")


def render_preview(user, site_id, revision_id, page_id):
    """Relire les droits, le contenu épinglé et le moteur à chaque consultation."""
    try:
        revision = lire_revision(user, site_id, revision_id)
        if revision["status"] != "ok":
            raise PreviewError("incompatible")
        document = revision["document"]
        page = next((p for p in document["pages"] if p["id"] == str(page_id)), None)
        if not page:
            raise PreviewError("inaccessible")
        attempt, profile = _connection(site_id)
        dependencies, block_ids = _dependencies(user, site_id, profile.instance_id, page, document["theme"])
        # Menu targets require the IDs of neighbouring pages, not their private contents.
        page_document = {**document, "pages": [p if p["id"] == page["id"] else {"id": p["id"]}
                                                for p in document["pages"]]}
        payload = {"site_id": revision["site_id"], "instance_id": str(profile.instance_id),
                   "revision_id": revision["id"], "revision_number": revision["number"],
                   "page_id": page["id"], "document": page_document, **dependencies}
        result = read_preview(profile, payload)
        _verify_result(profile, result, payload, block_ids)
        # A grant, media or connection may have been invalidated during the network round trip.
        catalogue._read(user, site_id)
        if _connection(site_id) != (attempt, profile):
            raise PreviewError("identity")
        if dependencies["media"] and SiteMedia.objects.filter(
            site_id=site_id, pk__in=dependencies["media"], active=True, asset=catalogue.DEMO_ASSET
        ).count() != len(dependencies["media"]):
            raise PreviewError("inaccessible")
        return result
    except Http404:
        raise PreviewError("inaccessible") from None
    except DatabaseError:
        raise PreviewError("unavailable") from None
    except (AttributeError, KeyError, TypeError, ValueError, RecursionError, UnicodeError, ValidationError):
        # Historic documents and partially upgraded renderers fail closed.
        raise PreviewError("incompatible") from None
    except ProbeError as error:
        code = error.code if error.code in PreviewError.messages else "unavailable"
        raise PreviewError(code) from None
