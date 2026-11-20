"""Brouillons du Studio central, autorisés et versionnés par site."""
import re
from dataclasses import dataclass
from uuid import UUID, uuid4

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.http import Http404

from registre.models import Site, SiteGrant
from registre.services import Conflict
from workspace.access import OPERATOR_GROUP

from .models import CompositionRevision
from .navigation import check_impact, navigation_candidate
from .validation import (MAX_MENU_ITEMS, SUPPORTED_VERSIONS, check_document,
                         check_navigation_document, remap_occurrence_ids, _check_document)


def _uuid(value):
    if isinstance(value, UUID):
        return value
    if isinstance(value, str):
        try:
            return UUID(value)
        except ValueError:
            pass
    return None


def _actor_id(actor):
    if not actor.is_authenticated or actor.pk is None:
        raise Http404
    return actor.pk


def _readable_sites(actor, site_id):
    return SiteGrant.objects.filter(
        site_id=site_id, user_id=_actor_id(actor),
        user__is_active=True, user__groups__name=OPERATOR_GROUP,
    ).values("site_id")


def _writing_site(actor, site_id):
    # Same first lock as registre_access, then the actual membership and grant rows.
    User = get_user_model()
    user_id = _actor_id(actor)
    if not User.objects.select_for_update().filter(pk=user_id, is_active=True).exists():
        raise Http404
    membership = User.groups.through.objects.select_for_update(of=("self",)).filter(
        user_id=user_id, group__name=OPERATOR_GROUP,
    )
    # Select a membership column so PostgreSQL locks only this membership.
    if membership.values_list("pk", flat=True).first() is None:
        raise Http404
    site = Site.objects.select_for_update().filter(pk=_uuid(site_id)).first()
    if site is None:
        raise Http404
    level = SiteGrant.objects.select_for_update().filter(
        site=site, user_id=user_id,
    ).values_list("level", flat=True).first()
    if level is None:
        raise Http404
    if level != "manage":
        raise PermissionDenied
    return site


def _schema_version(row):
    value = row.document.get("schema_version") if isinstance(row.document, dict) else None
    return value if type(value) is int else None


def _envelope(row):
    version = _schema_version(row)
    origin = row.origin if row.number == 1 else CompositionRevision.objects.values_list(
        "origin", flat=True
    ).get(site_id=row.site_id, number=1)
    return {
        "id": str(row.pk), "site_id": str(row.site_id), "number": row.number,
        "parent_id": str(row.parent_id) if row.parent_id else None,
        "author_id": row.author_id, "created_at": row.created_at.isoformat(),
        "schema_version": version, "origin": origin,
        "status": "ok" if version in SUPPORTED_VERSIONS else "incompatible",
        "document": row.document if version in SUPPORTED_VERSIONS else None,
    }


def lire_brouillon(acteur, site_id):
    sites = _readable_sites(acteur, _uuid(site_id))
    row = CompositionRevision.objects.filter(site_id__in=sites).order_by("-number").first()
    if row is None:
        if not sites.exists():
            raise Http404
        return None
    return _envelope(row)


def lire_revision(acteur, site_id, revision_id):
    sites = _readable_sites(acteur, _uuid(site_id))
    row = CompositionRevision.objects.filter(site_id__in=sites, pk=_uuid(revision_id)).first()
    if row is None:
        raise Http404
    return _envelope(row)


def _initial_document(site, origin, document, resolve_origin):
    if origin == {"kind": "blank"}:
        if document is not None:
            return document
        return {
            "schema_version": 1,
            "pages": [{"id": str(uuid4()), "parent_id": None, "slug": "",
                       "title": "Accueil", "sections": []}],
            "menus": [], "theme": {},
        }
    # Providers are trusted local adapters. Store only their opaque source coordinates.
    if not isinstance(origin, dict) or set(origin) != {"kind", "ref", "version"}:
        raise ValidationError("Origine invalide.", code="invalid_origin")
    if origin["kind"] not in ("template", "figma") or not all(
        isinstance(origin[key], str) and re.fullmatch(r"[A-Za-z0-9_.:-]{1,128}", origin[key])
        for key in ("ref", "version")
    ):
        raise ValidationError("Origine invalide.", code="invalid_origin")
    if document is not None or resolve_origin is None:
        raise ValidationError("Origine indisponible.", code="invalid_origin")
    source = resolve_origin(site.pk, origin.copy())
    if source is None:
        raise ValidationError("Origine indisponible.", code="invalid_origin")
    return source


@dataclass(frozen=True)
class ScopedComposition:
    """Origin returned by a trusted template resolver with private site dependencies."""
    site_id: UUID
    document: dict


def _has_private_refs(value):
    if isinstance(value, list):
        return any(_has_private_refs(item) for item in value)
    if isinstance(value, dict):
        if value.get("scope") == "site" or value.get("kind") in ("media", "wagtail_content"):
            return True
        return any(_has_private_refs(item) for item in value.values())
    return False


@transaction.atomic
def creer_brouillon(acteur, site_id, origine, document=None, *, resolve_origin=None,
                    resolve_definition=None, resolve_reference=None, occurrence_map=None):
    site = _writing_site(acteur, site_id)
    if CompositionRevision.objects.filter(site=site).exists():
        raise Conflict("Un brouillon existe déjà. Relisez la dernière révision.")
    source = _initial_document(site, origine, document, resolve_origin)
    source_site = None
    if isinstance(source, ScopedComposition) and origine["kind"] != "blank":
        source_site, source = _uuid(source.site_id), source.document
    checked = check_document(source, site.pk, resolve_definition=resolve_definition,
                             resolve_reference=resolve_reference)
    if origine["kind"] == "blank" and _editorial_bindings(checked):
        raise ValidationError("Vérifiez puis confirmez la référence éditoriale.")
    if origine["kind"] != "blank":
        if checked["schema_version"] >= 3 and _has_private_refs(checked) and source_site != site.pk:
            raise ValidationError("Origine privée non autorisée pour ce site.", code="invalid_origin")
        checked = remap_occurrence_ids(checked, occurrence_map)
        if checked["schema_version"] >= 2:
            checked = check_document(checked, site.pk, resolve_definition=resolve_definition,
                                     resolve_reference=resolve_reference)
    row = CompositionRevision.objects.create(
        site=site, number=1, author=acteur, origin=origine, document=checked,
    )
    return _envelope(row)


def _current_head(site, revision_de_base):
    head = CompositionRevision.objects.filter(site=site).order_by("-number").first()
    if head is None or head.pk != _uuid(revision_de_base):
        raise Conflict("Le brouillon a changé. Relisez la dernière révision.")
    if _schema_version(head) not in SUPPORTED_VERSIONS:
        raise ValidationError("Schéma du brouillon incompatible.", code="incompatible")
    return head


def _decisions(resolutions):
    if resolutions is None:
        return {}
    if not isinstance(resolutions, dict) or len(resolutions) > MAX_MENU_ITEMS or any(
        not isinstance(k, str) or not isinstance(v, str) or len(k) > 36 or len(v) > 36
        for k, v in resolutions.items()
    ):
        raise ValidationError("Les résolutions de navigation sont invalides.", code="invalid_navigation")
    return resolutions


def _editorial_bindings(document):
    from .appearance_contract import block_lists
    return {(page["id"], block["id"], name, value["ref_id"])
            for page, _, block in block_lists(document)
            for name, value in block["props"].items()
            if isinstance(value, dict) and value.get("kind") == "wagtail_content"}


def _save(actor, site, head, checked, decisions, confirmation, *, editorial_binding=None):
    if _editorial_bindings(checked) - _editorial_bindings(head.document) - {editorial_binding}:
        raise ValidationError("Vérifiez puis confirmez la référence éditoriale.")
    if checked["schema_version"] < _schema_version(head):
        raise ValidationError("Le brouillon doit conserver sa version de schéma.", code="incompatible")
    if checked["schema_version"] >= 2:
        if checked == {**head.document, "schema_version": checked["schema_version"]}:
            return _envelope(head)
        check_impact(head, checked, decisions, confirmation)
    row = CompositionRevision.objects.create(
        site=site, number=head.number + 1, parent=head, author=actor, document=checked,
    )
    return _envelope(row)


@transaction.atomic
def enregistrer_brouillon(acteur, site_id, revision_de_base, document, *, confirmation=None,
                          resolutions=None, resolve_definition=None, resolve_reference=None):
    site = _writing_site(acteur, site_id)
    head = _current_head(site, revision_de_base)
    checked = _check_document(document, site.pk, resolve_definition, resolve_reference, {}, head.document)
    return _save(acteur, site, head, checked, _decisions(resolutions), confirmation)


@transaction.atomic
def modifier_navigation(acteur, site_id, revision_de_base, commande, *, confirmation=None,
                        resolutions=None, resolve_definition=None, resolve_reference=None):
    """Apply one site-scoped command, or return its reproducible impact via ImpactRequired."""
    site = _writing_site(acteur, site_id)
    head = _current_head(site, revision_de_base)
    decisions = _decisions(resolutions)
    candidate = navigation_candidate(head.document, commande, decisions)
    if commande["action"] == "page_delete":
        # Unresolved links are present in the first diagnostic, never in a stored revision.
        check_impact(head, candidate, decisions, confirmation)
    checked = check_navigation_document(candidate, site.pk, head.document,
                                        resolve_definition=resolve_definition,
                                        resolve_reference=resolve_reference)
    return _save(acteur, site, head, checked, decisions, confirmation)

@transaction.atomic
def ajouter_pages_importees(actor, site_id, base_revision, document):
    """Append imported pages while preserving old opaque blocks byte-for-byte."""
    site = _writing_site(actor, site_id)
    head = _current_head(site, base_revision)
    old = head.document
    if (document["pages"][:len(old["pages"])] != old["pages"]
            or len(document["pages"]) <= len(old["pages"])
            or document["menus"] != old["menus"] or document["theme"] != old["theme"]):
        raise ValidationError("Un import doit conserver les pages, menus et réglages existants.")
    checked = check_navigation_document(document, site.pk, old)
    return _save(actor, site, head, checked, {}, None)
