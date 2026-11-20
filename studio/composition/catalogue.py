"""Catalogue de capacités livrées dans Studio et revue privée de leurs promotions."""
from hashlib import sha256
from pathlib import Path
import json
import re

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import Http404
from django.utils import timezone

from registre.models import Site
from registre.services import can_manage
from .catalogue_v1 import PARAMETERS, manifest
from .models import ComponentVersion, EditorialReference, Promotion, SiteMedia
from .services import _actor_id, _readable_sites, _uuid, _writing_site


REVIEW_GROUP = "Réviseurs du catalogue Studio"
DEMO_ASSET = "nuancier"
DEMO_LABEL = "Étude de formes"
DEMO_RIGHTS = "Illustration géométrique originale réalisée pour Studio, distribuable avec le projet et ses sites de démonstration."


def _read(actor, site_id):
    if not _readable_sites(actor, _uuid(site_id)).exists():
        raise Http404


def _record(row):
    return {**row.manifest, "id": str(row.pk), "scope": "site" if row.site_id else "global",
            "key": row.key, "version": row.version, "label": row.label, "renderer": row.renderer,
            "origin": row.origin, "retired": row.retired}


def definitions_du_site(site_id):
    return [_record(row) for row in ComponentVersion.objects.filter(Q(site_id=site_id) | Q(site=None))]


def definition(site_id, scope, key, version):
    if scope not in ("global", "site") or (scope == "site" and not site_id):
        return None
    row = ComponentVersion.objects.filter(site_id=site_id if scope == "site" else None,
                                          key=key, version=version).first()
    return _record(row) if row else None


def reference(site_id, kind, ref_id):
    if kind == "wagtail_content":
        return EditorialReference.objects.filter(site_id=site_id, pk=_uuid(ref_id)).exists()
    return kind == "media" and SiteMedia.objects.filter(site_id=site_id, pk=_uuid(ref_id),
                                                        asset=DEMO_ASSET, active=True).exists()


def bibliotheque(acteur, site_id):
    _read(acteur, site_id)
    site = Site.objects.get(pk=site_id)
    manage = can_manage(acteur, site)
    can_review = manage and acteur.groups.filter(name=REVIEW_GROUP).exists()
    proposals = Promotion.objects.filter(source__site=site).select_related("source", "result").order_by("-created_at")
    if not can_review:
        proposals = proposals.filter(author=acteur) if manage else proposals.none()
    return {"definitions": definitions_du_site(site_id),
            "medias": [{"id": str(key), "label": DEMO_LABEL} for key in SiteMedia.objects.filter(
                site=site, asset=DEMO_ASSET, active=True).values_list("pk", flat=True)],
            "promotions": list(proposals), "can_review": can_review}


def media_png(acteur, site_id, media_id):
    _read(acteur, site_id)
    if not reference(site_id, "media", media_id):
        raise Http404
    return (Path(__file__).parent / "assets" / "nuancier.png").read_bytes()


@transaction.atomic
def attribuer_media(site, *, actif=True):
    """Commande technique exécutée par l’équipe ayant accès au poste."""
    Site.objects.select_for_update().get(pk=site.pk)
    row, _ = SiteMedia.objects.update_or_create(site=site, asset=DEMO_ASSET, defaults={"active": actif})
    return row


def _text(value, maximum):
    if not isinstance(value, str) or not (1 <= len(value.strip()) <= maximum):
        raise ValidationError("Une valeur obligatoire est absente ou dépasse la longueur autorisée.")
    return value.strip()


def _key(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", value):
        raise ValidationError("La clé doit contenir des lettres minuscules, chiffres ou tirets.")
    return value


def installer_version(site, key, version, label, renderer):
    """Point d’entrée technique des livraisons. Aucun manifeste exécutable reçu."""
    if renderer not in PARAMETERS or type(version) is not int or not 1 <= version <= 2147483647:
        raise ValidationError("Rendu ou version non pris en charge.")
    defaults = dict(label=_text(label, 120), renderer=renderer, manifest=manifest(renderer),
                    origin="sur_mesure" if site else "standard")
    row, created = ComponentVersion.objects.get_or_create(site=site, key=_key(key), version=version, defaults=defaults)
    if not created and any(getattr(row, k) != v for k, v in defaults.items()):
        raise ValidationError("Cette version a déjà été livrée avec un autre manifeste.")
    return row


def _fingerprint(proposal):
    source = proposal.source
    content = [str(source.pk), str(source.site_id), source.key, source.version, source.renderer,
               source.manifest, proposal.key, proposal.version, proposal.label, proposal.rights,
               proposal.reason, proposal.author_id]
    return sha256(json.dumps(content, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _next_version(source, key):
    latest = ComponentVersion.objects.filter(site=None, key=key).order_by("-version").first()
    if not latest:
        return 1
    if not Promotion.objects.filter(result=latest, state="accepted", source__site_id=source.site_id,
                                    source__key=source.key, source__version__lt=source.version).exists():
        raise ValidationError("Cette clé partagée est déjà réservée. Choisissez une autre clé.")
    return latest.version + 1


@transaction.atomic
def proposer(acteur, site_id, definition_id, *, key, label, rights, reason):
    site = _writing_site(acteur, site_id)
    source = ComponentVersion.objects.select_for_update().filter(pk=_uuid(definition_id), site=site, retired=False).first()
    if not source:
        raise Http404
    key = _key(key)
    proposal = Promotion(source=source, author=acteur, key=key, label=_text(label, 120),
                         version=_next_version(source, key), rights=_text(rights, 500), reason=_text(reason, 500))
    proposal.fingerprint = _fingerprint(proposal)
    prior = Promotion.objects.filter(fingerprint=proposal.fingerprint, state="pending").first()
    if prior:
        return prior
    proposal.save()
    return proposal


@transaction.atomic
def examiner(acteur, site_id, promotion_id, *, fingerprint, approve, note, rights_checked=False, technical_checked=False):
    # Lock both users in stable order before locking their memberships and the site.
    # Grant administration uses the user as its first lock as well.
    author_id = Promotion.objects.filter(pk=_uuid(promotion_id), source__site_id=_uuid(site_id)).values_list(
        "author_id", flat=True).first()
    list(get_user_model().objects.select_for_update().filter(pk__in=[_actor_id(acteur), author_id])
         .order_by("pk").values_list("pk", flat=True))
    site = _writing_site(acteur, site_id)
    memberships = get_user_model().groups.through.objects.select_for_update(of=("self",))
    if not memberships.filter(user=acteur, group__name=REVIEW_GROUP).values_list("pk", flat=True).first():
        raise PermissionDenied
    proposal = Promotion.objects.select_for_update(of=("self",)).filter(
        pk=_uuid(promotion_id), source__site=site).select_related("source").first()
    if not proposal:
        raise Http404
    if proposal.author_id == acteur.pk:
        raise PermissionDenied
    if type(approve) is not bool or fingerprint != proposal.fingerprint or fingerprint != _fingerprint(proposal):
        raise ValidationError("Ce dossier a changé. Examinez une nouvelle proposition.")
    state = "accepted" if approve else "rejected"
    if proposal.state == state:
        return proposal
    if proposal.state != "pending":
        raise ValidationError("Ce dossier a déjà fait l’objet d’une autre décision.")
    proposal.note = _text(note, 500)
    if approve:
        if rights_checked is not True or technical_checked is not True:
            raise ValidationError("Vérifiez la preuve des droits et la copie technique avant d’accepter.")
        source = ComponentVersion.objects.select_for_update().get(pk=proposal.source_id)
        try:
            _writing_site(proposal.author, site_id)
        except (PermissionDenied, Http404):
            raise ValidationError("Le mandat de la proposition a été retiré.") from None
        proposal.source = source
        if (source.retired or proposal.fingerprint != _fingerprint(proposal) or source.renderer not in PARAMETERS
                or source.manifest != manifest(source.renderer)
                or _next_version(source, proposal.key) != proposal.version):
            raise ValidationError("La version candidate a changé ou son rendu est indisponible.")
        # Seules les propriétés et variantes du rendu redistribuable livré dans le code sont reprises.
        try:
            with transaction.atomic():
                proposal.result = ComponentVersion.objects.create(
                    site=None, key=proposal.key, version=proposal.version, label=proposal.label,
                    renderer=source.renderer, manifest=manifest(source.renderer), origin="promotion_revue")
        except IntegrityError:
            raise ValidationError("Cette version partagée existe désormais. Réexaminez le dossier.") from None
    proposal.state = state
    proposal.reviewer = acteur
    proposal.decided_at = timezone.now()
    proposal.save(update_fields=["note", "result", "state", "reviewer", "decided_at"])
    return proposal
