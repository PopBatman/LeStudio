"""Invitations, remises de conception et droits sur le site destinataire."""
import hashlib
import math
import re
import secrets
from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlsplit

from django.core import signing
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.utils.crypto import salted_hmac

from composition.services import _readable_sites, _uuid, _writing_site
from registre.services import Conflict

from .models import ExchangeWindow, FrameReference, ImportAnalysis, Invitation, PortalSession, Submission


WINDOW = timedelta(minutes=10)
RETENTION = timedelta(days=90)
CURSOR_SALT = "depots.history.cursor.v1"


class InvalidInvitation(Exception):
    pass


class RateLimited(Exception):
    def __init__(self, retry_after=None):
        self.retry_after = retry_after


def _digest(secret):
    if not isinstance(secret, str) or not re.fullmatch(r"[A-Za-z0-9_-]{43}", secret):
        raise InvalidInvitation
    return hashlib.sha256(secret.encode("ascii")).hexdigest()


@transaction.atomic
def create_invitation(actor, site_id):
    site = _writing_site(actor, site_id)
    secret = secrets.token_urlsafe(32)
    now = timezone.now()
    invitation = Invitation.objects.create(site=site, author_id=actor.pk, created_at=now,
        secret_digest=_digest(secret), expires_at=now + timedelta(days=7))
    return invitation, secret


@transaction.atomic
def revoke_invitation(actor, site_id, invitation_id):
    site = _writing_site(actor, site_id)
    invitation = Invitation.objects.select_for_update().filter(site=site, pk=_uuid(invitation_id)).first()
    if invitation is None:
        raise Http404
    if invitation.revoked_at is None:
        invitation.revoked_at = timezone.now()
        invitation.secret_digest = None
        invitation.save(update_fields=["revoked_at", "secret_digest"])
        PortalSession.objects.filter(invitation=invitation).delete()
    return invitation


def _retry_until(end, now):
    return max(1, math.ceil((end - now).total_seconds()))


@transaction.atomic
def _count_exchange(address):
    # Retain only a keyed fingerprint of the direct peer during its short window.
    key = salted_hmac("depots.exchange.peer", address or "", algorithm="sha256").hexdigest()
    row, _ = ExchangeWindow.objects.select_for_update().get_or_create(address_digest=key,
        defaults={"started_at": timezone.now()})
    now = timezone.now()
    if row.started_at + WINDOW <= now:
        row.started_at, row.attempts = now, 0
    if row.attempts >= 10:
        raise RateLimited(_retry_until(row.started_at + WINDOW, now))
    row.attempts += 1
    row.save(update_fields=["started_at", "attempts"])


def exchange(secret, address):
    # Charge attempts even when the following exchange fails.
    _count_exchange(address)
    with transaction.atomic():
        invitation = Invitation.objects.select_for_update().filter(secret_digest=_digest(secret)).first()
        if invitation is None or not invitation.active:
            raise InvalidInvitation
        cap = secrets.token_urlsafe(32)
        expiry = min(invitation.expires_at, timezone.now() + timedelta(hours=1))
        PortalSession.objects.create(invitation=invitation, digest=_digest(cap), expires_at=expiry)
        return cap, expiry


def _capability(secret, *, lock=False):
    # Lock invitations before observing session validity, as in revoke_invitation.
    invites = Invitation.objects
    if lock:
        invites = invites.select_for_update(of=("self",))
    invite = invites.filter(portalsession__pk=_digest(secret)).first()
    if invite is None or not invite.active or not PortalSession.objects.filter(
            invitation=invite, pk=_digest(secret), expires_at__gt=timezone.now()).exists():
        raise InvalidInvitation
    return invite


def invitation_for(capability_secret):
    return _capability(capability_secret)


def _figma_url(value):
    message = {"figma_url": "Saisissez un lien HTTPS vers un fichier de conception Figma."}
    if (not isinstance(value, str) or len(value) > 2048 or
            any(ord(c) < 32 or ord(c) == 127 for c in value)):
        raise ValidationError(message)
    try:
        url = urlsplit(value.strip())
        if (url.scheme != "https" or not re.fullmatch(r"(?:www\.)?figma\.com(?::443)?",
                url.netloc, flags=re.I)):
            raise ValueError
        path = re.fullmatch(r"/(?:file|design)/([A-Za-z0-9]+)(?:/[^/]*)?/?", url.path)
        if not path:
            raise ValueError
        nodes = parse_qs(url.query, keep_blank_values=True).get("node-id", [])
        canonical = f"https://www.figma.com/design/{path[1]}"
        if nodes:
            if len(nodes) != 1 or not re.fullmatch(r"[0-9]+[:-][0-9]+", nodes[0]):
                raise ValidationError({"figma_url": "Le numéro de nœud Figma est invalide."})
            canonical += "?node-id=" + nodes[0].replace(":", "-")
        if len(canonical) > 2048:
            raise ValueError
        return canonical
    except ValueError:
        raise ValidationError(message) from None


@transaction.atomic
def submit(capability_secret, request_id, figma_url, comment=""):
    invitation = _capability(capability_secret, lock=True)
    key = _uuid(request_id)
    if key is None:
        raise ValidationError("Rouvrez le formulaire de dépôt.")
    url = _figma_url(figma_url)
    if not isinstance(comment, str) or len(comment) > 2000 or "\x00" in comment:
        raise ValidationError({"comment": "Saisissez un commentaire de 2 000 caractères maximum."})
    comment = comment.strip()
    existing = Submission.objects.filter(invitation=invitation, request_id=key).first()
    if existing:
        if existing.erased_at is not None or (existing.figma_url, existing.comment) != (url, comment):
            raise Conflict("Ce formulaire a déjà été utilisé. Ouvrez une nouvelle remise.")
        return existing
    if invitation.last_version >= 20:
        raise RateLimited()
    now = timezone.now()
    recent = Submission.objects.filter(invitation=invitation, created_at__gt=now-WINDOW)
    if recent.count() >= 5:
        raise RateLimited(_retry_until(recent.earliest("created_at").created_at + WINDOW, now))
    invitation.last_version += 1
    invitation.save(update_fields=["last_version"])
    return Submission.objects.create(invitation=invitation, version=invitation.last_version,
        created_at=now, request_id=key, figma_url=url, comment=comment)


def _visible_submissions():
    return Submission.objects.filter(erased_at__isnull=True, created_at__gt=timezone.now()-RETENTION)


def receipt(capability_secret, submission_id):
    invitation = invitation_for(capability_secret)
    row = _visible_submissions().filter(invitation=invitation, pk=_uuid(submission_id)).first()
    if row is None:
        raise Http404
    return row


def _access(actor, site_id):
    sites = _readable_sites(actor, _uuid(site_id))
    if not sites.exists():
        raise Http404
    return sites


def invitations(actor, site_id):
    return Invitation.objects.filter(site_id__in=_access(actor, site_id)).order_by("-created_at", "-pk")


def _rows(actor, site_id):
    return _visible_submissions().filter(invitation__site_id__in=_access(actor, site_id)).select_related(
        "invitation").order_by("-created_at", "-pk")


def latest_submission(actor, site_id):
    return _rows(actor, site_id).first()


def submissions(actor, site_id, cursor=None):
    rows = _rows(actor, site_id)
    if cursor:
        try:
            if len(cursor) > 512:
                raise ValueError
            scope, position, identity = signing.loads(cursor, salt=CURSOR_SALT)
            date = datetime.fromisoformat(position)
            if scope != str(site_id) or not timezone.is_aware(date) or _uuid(identity) is None:
                raise ValueError
        except (TypeError, ValueError, signing.BadSignature):
            raise ValidationError("Cette page de l’historique est indisponible.") from None
        rows = rows.filter(Q(created_at__lt=date) | Q(created_at=date, pk__lt=identity))
    items = list(rows[:21])
    following = None
    if len(items) == 21:
        last = items[19]
        following = signing.dumps([str(site_id), last.created_at.isoformat(), str(last.pk)], salt=CURSOR_SALT)
    return items[:20], following


def submission_for(actor, site_id, submission_id):
    row = _rows(actor, site_id).filter(pk=_uuid(submission_id)).first()
    if row is None:
        raise Http404
    return row


@transaction.atomic
def source_for_import(actor, site_id, submission_id):
    site = _writing_site(actor, site_id)
    row = submission_for(actor, site.pk, submission_id)
    return {"site_id": str(site.pk), "invitation_id": str(row.invitation_id),
            "submission_id": str(row.pk), "version": row.version, "created_at": row.created_at.isoformat(),
            "figma_url": row.figma_url, "comment": row.comment, "provenance": "invitation"}


@transaction.atomic
def erase_submission(actor, site_id, submission_id):
    site = _writing_site(actor, site_id)
    rows = Submission.objects.filter(invitation__site=site, pk=_uuid(submission_id))
    if not rows.exists():
        raise Http404
    list(rows.select_for_update().values_list("id", flat=True))
    _forget_imports(rows)
    rows.filter(erased_at__isnull=True).update(figma_url="", comment="", erased_at=timezone.now())


def _forget_imports(submissions):
    reviews = ImportAnalysis.objects.filter(submission__in=submissions)
    FrameReference.objects.filter(analysis__in=reviews).delete()
    reviews.filter(result_revision__isnull=True).delete()
    reviews.update(submission=None, generation="", version="", inventory={}, observation={},
                   proposals=[], decisions={}, destinations=[], mapping={}, error="", retry_at=None)


@transaction.atomic
def purge():
    now = timezone.now()
    expired_sources = Submission.objects.filter(created_at__lte=now-RETENTION)
    # Serialize erasure with an import that is finishing its remote read.
    sources = expired_sources.filter(erased_at__isnull=True)
    list(sources.select_for_update().order_by("pk").values_list("pk", flat=True))
    _forget_imports(expired_sources)
    erased = sources.update(
        figma_url="", comment="", erased_at=now)
    inactive = Q(expires_at__lte=now) | Q(revoked_at__isnull=False)
    expired = Invitation.objects.filter(inactive)
    expired.update(secret_digest=None)
    PortalSession.objects.filter(Q(expires_at__lte=now) | Q(invitation__in=expired)).delete()
    ExchangeWindow.objects.filter(started_at__lte=now-WINDOW).delete()
    # An active invitation retains erased request IDs to prevent re-creating erased content on retry.
    Submission.objects.filter(invitation__in=expired, erased_at__isnull=False).delete()
    expired.filter(submission__isnull=True).delete()
    return erased
