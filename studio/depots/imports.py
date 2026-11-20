"""Private Figma reviews. Remote reads occur outside every database transaction."""

from datetime import timedelta
import json
from uuid import UUID, uuid4

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.utils import timezone

from composition import figma_mapping
from composition.models import ComponentVersion, CompositionRevision, SiteMedia
from composition.services import ScopedComposition, ajouter_pages_importees, creer_brouillon
from registre.services import Conflict

from . import figma
from .models import ImportAnalysis, Submission
from .services import RETENTION, source_for_import


def _source(actor, site_id, submission_id):
    source = source_for_import(actor, site_id, submission_id)
    if (
        not Submission.objects.select_for_update()
        .filter(
            pk=source["submission_id"], erased_at__isnull=True, created_at__gt=timezone.now() - RETENTION
        )
        .exists()
    ):
        raise Http404
    return source


def _head(site):
    return CompositionRevision.objects.filter(site_id=site).order_by("-number").first()


def _head_id(site):
    return (
        CompositionRevision.objects.filter(site_id=site)
        .order_by("-number")
        .values_list("pk", flat=True)
        .first()
    )


def _row(source, token=None):
    row = ImportAnalysis.objects.select_for_update().filter(submission_id=source["submission_id"]).first()
    if token is not None and (not row or str(row.token) != str(token)):
        raise Conflict("La revue a changé. Rechargez la dernière décision.")
    return row


def _cooldown(row):
    if row and row.retry_at and row.retry_at > timezone.now():
        raise ValidationError(
            "Le quota de lecture est atteint. Réessayez après "
            + timezone.localtime(row.retry_at).strftime("%H:%M:%S")
            + "."
        )


def _fail(args, token, error):
    with transaction.atomic():
        source = _source(*args)
        row = _row(source, token)
        if row:
            if error.code in ("profile", "inaccessible", "changed") or row.state == "loading":
                row.inventory, row.observation, row.proposals = {}, {}, []
                row.decisions, row.destinations, row.mapping = {}, [], {}
                row.state = "applied" if row.result_revision_id else "failed"
                if not row.result_revision_id:
                    row.token = uuid4()
            row.error = str(error)[:256]
            if error.code == "limited":
                row.retry_at = timezone.now() + timedelta(seconds=error.retry_after or 60)
            row.save()
    raise ValidationError(str(error), code=error.code)


class _Changed(Exception):
    code = "changed"

    def __str__(self):
        return "La source ou son profil a changé. Recommencez l’analyse de la remise."


def _fresh(args, *, token=None, frames=None, begin=False):
    with transaction.atomic():
        source = _source(*args)
        row = _row(source, token)
        _cooldown(row)
        if begin and row and row.result_revision_id:
            begin = False
        if begin:
            if row and row.state == "loading" and row.updated_at > timezone.now() - timedelta(seconds=40):
                raise Conflict("Une lecture de cette remise est en cours.")
            row, _ = ImportAnalysis.objects.update_or_create(
                submission_id=source["submission_id"],
                defaults={
                    "state": "loading",
                    "token": uuid4(),
                    "base_revision_id": _head_id(source["site_id"]),
                    "inventory": {},
                    "observation": {},
                    "proposals": [],
                    "decisions": {},
                    "destinations": [],
                    "version": "",
                    "generation": "",
                    "error": "",
                    "retry_at": None,
                },
            )
        if not row:
            return None, None
        if frames is not None and row.state not in ("inventory", "review"):
            raise Conflict("Recommencez l’analyse avant de sélectionner des frames.")
        if not begin and row.state in ("failed", "loading"):
            return row, None
        marker = row.token
    try:
        profile = figma.load_profile(source["site_id"], source["figma_url"])
        if not begin and profile.generation != row.generation:
            raise _Changed()
        if frames is not None:
            if (
                not isinstance(frames, list)
                or not 1 <= len(frames) <= 8
                or any(
                    not isinstance(k, str) or k not in {f["id"] for f in row.inventory["frames"]}
                    for k in frames
                )
                or len(set(frames)) != len(frames)
            ):
                raise ValidationError("Choisissez entre une et huit frames de cet inventaire.")
            observed = figma.inspect_frames(profile, row.version, frames)
        else:
            observed = figma.inventory(profile)
        if not begin and observed["version"] != row.version:
            raise _Changed()
        with transaction.atomic():
            source = _source(*args)
            row = _row(source, marker)
            if figma.load_profile(source["site_id"], source["figma_url"]).generation != profile.generation:
                raise _Changed()
            if begin:
                row.inventory = observed
                row.generation = profile.generation
                row.version = observed["version"]
                row.state = "inventory"
                row.save()
            elif frames is not None:
                if row.result_revision_id:
                    raise Conflict("Cette proposition a déjà été intégrée.")
                row.observation = observed
                row.proposals = figma_mapping.propose(source["site_id"], observed)
                row.decisions, row.destinations = {}, []
                row.state, row.token, row.error = "review", uuid4(), ""
                row.base_revision_id = _head_id(source["site_id"])
                row.save()
            return row, profile
    except (figma.FigmaError, _Changed) as error:
        _fail(args, marker, error)


def start(actor, site_id, submission_id):
    return _fresh((actor, site_id, submission_id), begin=True)[0]


def current(actor, site_id, submission_id):
    return _fresh((actor, site_id, submission_id))[0]


def select_frames(actor, site_id, submission_id, token, frame_ids):
    if not token:
        raise Conflict("Rechargez la revue.")
    return _fresh((actor, site_id, submission_id), token=token, frames=frame_ids)[0]


def _review(args, token, profile):
    source = _source(*args)
    row = _row(source, token)
    if not row or row.state != "review" or not profile:
        raise Conflict("Reprenez la sélection des frames avant de confirmer.")
    if figma.load_profile(source["site_id"], source["figma_url"]).generation != profile.generation:
        raise _Changed()
    return row


def save_review(actor, site_id, submission_id, token, decisions, destinations):
    args = actor, site_id, submission_id
    if not token or not isinstance(decisions, dict) or not isinstance(destinations, list):
        raise ValidationError("Décisions de revue invalides.")
    if (
        len(decisions) > 2000
        or len(destinations) > 8
        or len(json.dumps([decisions, destinations]).encode()) > 1048576
    ):
        raise ValidationError("La revue dépasse la taille prise en charge.")
    _, profile = _fresh(args, token=token)
    try:
        with transaction.atomic():
            row = _review(args, token, profile)
            allowed_ids = {item["id"] for item in row.proposals}
            if any(
                k not in allowed_ids
                or not isinstance(v, dict)
                or v.get("action") not in ("accept", "correct", "exclude")
                for k, v in decisions.items()
            ):
                raise ValidationError("Vérifiez les décisions de cette sélection.")
            row.decisions, row.destinations, row.token = decisions, destinations, uuid4()
            row.save()
            return row
    except (figma.FigmaError, _Changed) as error:
        _fail(args, token, error)


def _receipt(row):
    # A retry needs only the committed local revision, even during a provider outage.
    row.inventory, row.observation, row.proposals, row.mapping = {}, {}, [], {}
    row.destinations, row.decisions = [], {}
    return row


def confirm(actor, site_id, submission_id, token):
    if not token:
        raise Conflict("Rechargez la revue.")
    args = actor, site_id, submission_id
    with transaction.atomic():
        row = _row(_source(*args), token)
        if row and row.result_revision_id:
            return _receipt(row)
    row, profile = _fresh(args, token=token)
    try:
        with transaction.atomic():
            source = _source(*args)
            row = _row(source, token)
            if row and row.result_revision_id:
                return _receipt(row)
            row = _review(args, token, profile)
            head = _head(site_id)
            if (head.pk if head else None) != row.base_revision_id:
                raise Conflict("Le brouillon a changé. Reprenez la sélection et la comparaison.")
            # Pin mutable catalogue availability and media ownership until the revision commits.
            list(
                ComponentVersion.objects.select_for_update()
                .filter(Q(site_id=site_id) | Q(site=None))
                .order_by("pk")
                .values_list("pk", flat=True)
            )
            list(
                SiteMedia.objects.select_for_update()
                .filter(site_id=site_id)
                .order_by("pk")
                .values_list("pk", flat=True)
            )
            if figma_mapping.propose(site_id, row.observation) != row.proposals:
                raise Conflict("Le catalogue a changé. Reprenez la comparaison.")
            document, mapping = figma_mapping.project(
                site_id,
                row.observation,
                row.proposals,
                row.decisions,
                row.destinations,
                head.document if head else None,
            )
            if head:
                revision = ajouter_pages_importees(actor, site_id, head.pk, document)
            else:
                key = {"kind": "figma", "ref": str(row.pk), "version": str(row.token)}
                remap = {}
                revision = creer_brouillon(
                    actor,
                    site_id,
                    key,
                    occurrence_map=remap,
                    resolve_origin=lambda site, origin: (
                        ScopedComposition(site, document)
                        if (str(site) == source["site_id"] and origin == key)
                        else None
                    ),
                )
                mapping = {node: remap[local] for node, local in mapping.items()}
            row.state, row.result_revision_id, row.mapping = "applied", UUID(revision["id"]), mapping
            row.save()
            return row
    except (figma.FigmaError, _Changed) as error:
        _fail(args, token, error)
