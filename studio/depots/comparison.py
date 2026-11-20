"""Private frame exports and operator decisions about a verified Studio draft."""
from hashlib import sha256
from io import BytesIO

from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import Http404
from django.utils import timezone
from PIL import Image, UnidentifiedImageError

from composition import preview_views
from composition.models import PreviewTicket
from composition.services import _current_head, _uuid, _writing_site
from registre.services import Conflict

from .models import ComparisonDecision, FrameReference, ImportAnalysis
from .provenance import frame_metadata
from .services import _visible_submissions


MAX_FILE_BYTES = 6 * 1024 * 1024
MAX_PIXELS = 12_000_000
MAX_DIMENSION = 16_384


def _normalized_png(upload):
    if not hasattr(upload, "read") or getattr(upload, "size", 0) > MAX_FILE_BYTES:
        raise ValidationError("Fournissez un export PNG de 6 Mio maximum.")
    contents = upload.read(MAX_FILE_BYTES + 1)
    if not contents or len(contents) > MAX_FILE_BYTES:
        raise ValidationError("Fournissez un export PNG de 6 Mio maximum.")
    try:
        with Image.open(BytesIO(contents), formats=("PNG",)) as image:
            width, height = image.size
            if max(width, height) > MAX_DIMENSION or width * height > MAX_PIXELS:
                raise ValidationError("L’export dépasse les limites de dimensions du PNG.")
            if image.is_animated:
                raise ValidationError("Fournissez un PNG statique.")
            image.verify()
        # Decode every pixel, expand palettes/transparency and strip all metadata.
        with Image.open(BytesIO(contents), formats=("PNG",)) as image:
            clean = image.convert("RGBA")
            clean.info.clear()
            output = BytesIO()
            clean.save(output, format="PNG")
        if len(output.getbuffer()) > MAX_FILE_BYTES:
            raise ValidationError("Le PNG normalisé dépasse 6 Mio.")
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError, Image.DecompressionBombError):
        raise ValidationError("L’export PNG est illisible ou incomplet.") from None
    return output.getvalue(), width, height


def _live_frame(site_id, analysis_id, page_id, frame_id):
    # Lock the submission before its analysis, in the order used by the retention job.
    submission = _visible_submissions().select_for_update(of=("self",)).filter(
        importanalysis__pk=_uuid(analysis_id), invitation__site_id=site_id).first()
    if not submission:
        raise Http404
    analysis = ImportAnalysis.objects.select_for_update(of=("self",)).select_related("submission").filter(
        pk=_uuid(analysis_id), state="applied", result_revision__site_id=site_id, submission=submission).first()
    if not analysis:
        raise Http404
    frame = next((frame for frame in frame_metadata(analysis, str(page_id)) if frame["id"] == frame_id), None)
    if not frame or not analysis.version:
        raise Http404
    return analysis, frame


def current_reference(analysis_id, frame_id):
    """Metadata only. The caller has established access to this active source."""
    return FrameReference.objects.defer("png").filter(
        analysis_id=analysis_id, frame_id=frame_id, png__isnull=False).first()


@transaction.atomic
def attach_reference(actor, site_id, analysis_id, page_id, frame_id, version, format, upload, *, revision_id, previous=""):
    site = _writing_site(actor, site_id)
    head = _current_head(site, revision_id)
    if not preview_views.lookup_page(head.document, str(page_id)):
        raise Http404
    analysis, frame = _live_frame(site.pk, analysis_id, page_id, frame_id)
    if analysis.version != version or frame["format"] != format:
        raise Conflict("La version ou le format de la frame a changé.")
    current = current_reference(analysis.pk, frame_id)
    if str(current.pk if current else "") != str(previous or ""):
        raise Conflict("La référence de cette frame a changé. Rechargez la comparaison.")
    png, width, height = _normalized_png(upload)
    fw, fh = frame["width"], frame["height"]
    if fw and fh and abs(width * fh - height * fw) > max(fw, fh, width, height):
        raise ValidationError("Le rapport largeur/hauteur du PNG ne correspond pas à la frame.")
    if current:
        FrameReference.objects.filter(pk=current.pk).update(png=None)
    return FrameReference.objects.create(
        analysis=analysis, page_id=page_id, frame_id=frame_id, version=version, format=format,
        digest=sha256(png).hexdigest(), png=png, width=width, height=height, author=actor)


@transaction.atomic
def reference_png(actor, site_id, reference_id):
    site = _writing_site(actor, site_id)
    row = FrameReference.objects.defer("png").filter(pk=_uuid(reference_id), png__isnull=False,
                                                    analysis__result_revision__site=site).first()
    if not row:
        raise Http404
    analysis, frame = _live_frame(site.pk, row.analysis_id, row.page_id, row.frame_id)
    if row.version != analysis.version or row.format != frame["format"]:
        raise Http404
    return bytes(row.png)


def save_decision(request, site_id, analysis_id, page_id, frame_id, *, reference_id, ticket_id,
                  revision_id, format, width, target, kind, note, previous="", key):
    """Check the remote render between two short authorization/commit transactions."""
    with transaction.atomic():
        _writing_site(request.user, site_id)
        _live_frame(site_id, analysis_id, page_id, frame_id)
    ticket = preview_views.get_ticket(request, site_id, _uuid(ticket_id))
    if ticket.page_id != _uuid(page_id) or ticket.revision_id != _uuid(revision_id):
        raise Conflict("Le reçu concerne une autre page ou révision.")
    result, error, _ = preview_views.verified(request, ticket)
    if not result:
        raise Conflict(error)

    if kind not in ("correct", "accepted", "matched"):
        raise ValidationError("Choisissez une décision de comparaison.")
    note = (note or "").strip()
    if len(note) > 1000 or (kind != "matched" and not note):
        raise ValidationError("Précisez un motif de 1 à 1 000 caractères.")
    if not _uuid(key) or (previous and not _uuid(previous)):
        raise ValidationError("L’identifiant de décision est invalide.")
    occurrence = _uuid(target)
    if target and (not occurrence or str(occurrence) not in result["manifest"]["block_ids"]):
        raise ValidationError("L’occurrence est absente du rendu vérifié.")
    try:
        logical_width = int(str(width))
    except (ValueError, TypeError):
        raise ValidationError("Largeur de comparaison invalide.") from None

    with transaction.atomic():
        site = _writing_site(request.user, site_id)
        analysis, frame = _live_frame(site.pk, analysis_id, page_id, frame_id)
        head = _current_head(site, revision_id)
        current = current_reference(analysis.pk, frame_id)
        if (not current or current.pk != _uuid(reference_id) or current.version != analysis.version
                or current.format != frame["format"] or current.format != format):
            raise Conflict("La référence a changé. Comparez la frame à nouveau.")
        if logical_width != frame["width"] or not 1 <= logical_width <= MAX_DIMENSION:
            raise ValidationError("La largeur affichée doit correspondre à la largeur logique de la frame.")
        now = timezone.now()
        # Logout deletes session and ticket. Compare their lifetimes again after rendering.
        session_ok = Session.objects.select_for_update().filter(
            pk=request.session.session_key, expire_date__gt=now).exists()
        ticket_ok = PreviewTicket.objects.select_for_update().filter(
            pk=ticket.pk, operator=request.user, session_id=request.session.session_key,
            expires_at__gt=now, fingerprint=ticket.fingerprint).exists()
        if not session_ok or not ticket_ok:
            raise Conflict("Le reçu a expiré. Préparez à nouveau le rendu.")
        values = dict(revision_id=head.pk, page_id=ticket.page_id, target=occurrence, kind=kind, note=note,
                      previous_id=_uuid(previous), width=logical_width, instance_id=_uuid(result["manifest"]["instance_id"]),
                      render_digest=ticket.fingerprint)
        retry = ComparisonDecision.objects.filter(reference=current, author=request.user, key=key).first()
        if retry:
            if any(getattr(retry, field) != value for field, value in values.items()):
                raise Conflict("Cette clé identifie une autre décision.")
            return retry
        latest = ComparisonDecision.objects.filter(
            reference__analysis=analysis, reference__frame_id=frame_id, page_id=ticket.page_id,
            reference__format=format, target=occurrence).first()
        if str(latest.pk if latest else "") != str(previous or ""):
            raise Conflict("Une décision plus récente existe pour cette cible. Relisez-la avant de décider.")
        return ComparisonDecision.objects.create(reference=current, author=request.user, key=key, **values)
