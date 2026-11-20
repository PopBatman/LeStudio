import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.utils import timezone
from registre.models import Site, SiteGrant
from registre.services import sites
from workspace.access import OPERATOR_GROUP

from .models import SiteConnection
from .profiles import load_profile, ProfileError
from .transport import probe, ProbeError


class LinkError(Exception):
    """A stable, non-sensitive diagnostic safe for the command line."""


def _manager(user_id, site_id):
    user = get_user_model().objects.select_for_update().filter(pk=user_id, is_active=True).first()
    if user is None or not user.groups.select_for_update().filter(name=OPERATOR_GROUP).exists():
        raise LinkError("not_found")
    site = Site.objects.select_for_update().filter(pk=site_id).first()
    if site is None:
        raise LinkError("not_found")
    level = SiteGrant.objects.select_for_update().filter(
        site_id=site_id, user_id=user_id
    ).values_list("level", flat=True).first()
    if level is None:
        raise LinkError("not_found")
    if level != "manage":
        raise LinkError("forbidden")
    return site


def _profile(alias, site_id):
    try:
        profile = load_profile(alias)
    except ProfileError:
        raise LinkError("invalid_profile") from None
    if profile.site_id != site_id:
        raise LinkError("identity_mismatch")
    return profile


def _snapshot(row):
    if row is None:
        return {"status": "unlinked", "confirmed": None, "attempt": None}
    confirmed = None
    if row.confirmed_at:
        versions = row.versions if isinstance(row.versions, dict) else {}
        fields = ("engine_version", "wagtail_version", "contract_major", "contract_minor", "image_digest")
        confirmed = {key: versions[key] for key in fields if key in versions}
        confirmed.update(at=row.confirmed_at.isoformat(),
                         instance_id=str(row.instance_id) if row.instance_id else None,
                         profile=row.confirmed_profile)
    code = row.diagnostic
    if not row.finished_at and row.expires_at <= timezone.now():
        code = "attempt_expired"
    return {"status": code, "confirmed": confirmed,
            "attempt": {"id": str(row.attempt_id), "started_at": row.started_at.isoformat(),
                        "finished_at": row.finished_at.isoformat() if row.finished_at else None}}


def inspect_link(user, site_id):
    site = sites(user).filter(pk=site_id).first()
    if site is None:
        raise LinkError("not_found")
    return _snapshot(SiteConnection.objects.filter(site=site).first())


def verify_link(user, site_id, alias):
    with transaction.atomic():
        site = _manager(user.pk, site_id)
        row = SiteConnection.objects.filter(site=site).first() or SiteConnection(site=site)
        now = timezone.now()
        if row.started_at and not row.finished_at and row.expires_at > now:
            raise LinkError("in_progress")
        token = uuid.uuid4()
        row.attempt_id = token
        row.actor_id = user.pk
        row.started_at = now
        row.expires_at = now + timedelta(seconds=20)
        row.finished_at = None
        row.diagnostic = "checking"
        row.save()

    try:
        profile = _profile(alias, site.pk)
        if row.instance_id and row.instance_id != profile.instance_id:
            raise LinkError("association_conflict")
        versions = probe(profile)
    except LinkError as error:
        code = str(error)
    except ProbeError as error:
        code = error.code
    else:
        code = "connected"

    with transaction.atomic():
        try:
            _manager(user.pk, site_id)
        except LinkError as error:
            code = str(error)
        row = SiteConnection.objects.select_for_update().get(site_id=site_id)
        if row.attempt_id != token:
            raise LinkError("superseded")
        now = timezone.now()
        if row.expires_at <= now:
            code = "attempt_expired"
        if code == "connected":
            try:
                if _profile(alias, site.pk) != profile:
                    raise LinkError("profile_changed")
                with transaction.atomic():
                    SiteConnection.objects.filter(pk=row.pk).update(
                        instance_id=profile.instance_id, confirmed_profile=profile.alias,
                        confirmed_at=now, versions=versions,
                    )
            except LinkError as error:
                code = str(error)
            except IntegrityError:
                code = "association_conflict"
        row.finished_at = now
        row.diagnostic = code
        row.save(update_fields=["finished_at", "diagnostic"])
        if code == "connected":
            row.refresh_from_db()
            return _snapshot(row)
    raise LinkError(code)


def editorial_admin_url(actor, site):
    """Browser destination of the current managed instance, without a network read."""
    with transaction.atomic():
        try:
            site = _manager(actor.pk, site.pk)
            row = SiteConnection.objects.filter(site=site, diagnostic="connected", confirmed_at__isnull=False).first()
            if row:
                profile = _profile(row.confirmed_profile, site.pk)
                if (row.instance_id == profile.instance_id
                        and row.versions.get("image_digest") == profile.image_digest
                        and row.versions.get("engine_version") == profile.engine_version):
                    return profile.admin_url
        except LinkError:
            pass
    return ""
