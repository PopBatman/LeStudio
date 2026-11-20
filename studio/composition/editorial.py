"""Association d’une occurrence Studio à une révision publique du moteur raccordé."""
from copy import deepcopy
from uuid import UUID, uuid4

from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import Http404
from django.utils import timezone

from raccordement.models import SiteConnection
from raccordement.profiles import ProfileError, load_profile
from raccordement.transport import ProbeError, read_published_article
from registre.services import Conflict

from .catalogue import _read, definition
from .editor import _apply, _block_location, _member
from .models import ComponentVersion, EditorialObservation, EditorialReference
from .services import _current_head, _save, _uuid, _writing_site
from .validation import _check_document


class SourceChanged(Exception):
    def __init__(self, observation):
        super().__init__("La source a changé. Vérifiez le résultat avant de confirmer.")
        self.observation = observation


def _available(link):
    return (link and link.instance_id and link.confirmed_at and link.diagnostic == "connected"
            and isinstance(link.versions, dict)
            and isinstance(link.versions.get("capabilities"), list)
            and "editorial.published.v1" in link.versions["capabilities"])


def _profile(link):
    if _available(link):
        try:
            profile = load_profile(link.confirmed_profile)
        except ProfileError:
            return None
        if (profile.site_id == link.site_id and profile.instance_id == link.instance_id
                and profile.engine_version == link.versions.get("engine_version")
                and profile.image_digest == link.versions.get("image_digest")):
            return profile
    return None


def _snapshot(obs):
    return {"token": str(obs.attempt), "page_number": obs.page_number,
            "published_revision": obs.published_revision or None, "status": obs.status,
            "checked_at": obs.checked_at, "last_success_at": obs.last_success_at}


def _offline(page_number):
    return {"token": "", "page_number": page_number, "published_revision": None,
            "status": "unavailable", "checked_at": timezone.now(), "last_success_at": None}


def _link(site_id):
    return SiteConnection.objects.select_for_update().filter(site_id=site_id).first()


def _read_page(actor, site_id, page_number, previous=None):
    with transaction.atomic():
        site = _writing_site(actor, site_id)
        if type(page_number) is not int or not 1 <= page_number <= 2147483647:
            raise ValidationError("Saisissez un identifiant de page positif valide.")
        link = _link(site.pk)
        if not link or not link.instance_id:
            return _offline(page_number), None
        obs, _ = EditorialObservation.objects.get_or_create(site=site, instance_id=link.instance_id,
            page_number=page_number, defaults={"status": "unverified", "connection_attempt": link.attempt_id})
        if previous and (str(obs.attempt) != previous["token"] or obs.connection_attempt != link.attempt_id):
            raise Conflict("L’observation a changé. Vérifiez à nouveau cet article.")
        attempt = uuid4()
        profile = _profile(link)
        obs.attempt, obs.connection_attempt = attempt, link.attempt_id
        obs.status, obs.published_revision, obs.checked_at = "unverified", "", None
        obs.save()

    status, revision = "unavailable", ""
    if profile:
        try:
            revision = read_published_article(profile, page_number)
            status = "ok"
        except ProbeError as exc:
            if exc.code == "inaccessible":
                status = "inaccessible"

    with transaction.atomic():
        site = _writing_site(actor, site_id)
        current = _link(site.pk)
        obs.refresh_from_db()
        if obs.attempt != attempt:
            raise Conflict("Une autre vérification de cet article a eu lieu.")
        if (not current or current.attempt_id != link.attempt_id or current.instance_id != link.instance_id
                or _profile(current) != profile):
            status, revision = "unavailable", ""
        obs.status, obs.published_revision, obs.checked_at = status, revision, timezone.now()
        if status == "ok":
            obs.last_success_at = obs.checked_at
        obs.save()
        return _snapshot(obs), profile


def verifier_article(actor, site_id, page_number):
    observation, _ = _read_page(actor, site_id, page_number)
    return observation


def lire_observation(actor, site_id, token):
    _read(actor, site_id)
    obs = EditorialObservation.objects.filter(site_id=site_id, attempt=_uuid(token)).first()
    if obs is None:
        raise Http404
    result = _snapshot(obs)
    link = SiteConnection.objects.filter(site_id=site_id).first()
    if not _profile(link) or link.instance_id != obs.instance_id or link.attempt_id != obs.connection_attempt:
        result.update(status="unavailable", published_revision=None)
    return result


def article_occurrence(actor, site_id, node):
    reference = node["props"].get("content")
    if isinstance(reference, dict) and reference.get("kind") == "wagtail_content":
        try:
            ref_id = UUID(str(reference.get("ref_id")))
        except ValueError:
            pass
        else:
            return lire_article(actor, site_id, ref_id)
    return {"status": "unverified"}


def lire_article(actor, site_id, ref_id):
    _read(actor, site_id)
    pin = EditorialReference.objects.filter(site_id=site_id, pk=_uuid(ref_id)).first()
    if not pin:
        return {"status":"inaccessible", "page_number":None, "expected_revision":None, "observation":None}
    link = SiteConnection.objects.filter(site_id=site_id).first()
    obs = EditorialObservation.objects.filter(site_id=site_id, instance_id=pin.instance_id,
                                             page_number=pin.page_number).first()
    observed = _snapshot(obs) if obs else None
    status = "unverified"
    if not _profile(link) or link.instance_id != pin.instance_id or (obs and obs.connection_attempt != link.attempt_id):
        status = "unavailable"
        if observed:
            observed.update(status=status, published_revision=None)
    elif obs:
        status = obs.status
        if status == "ok":
            status = "concordant" if pin.published_revision == obs.published_revision else "divergent"
    return {"page_number":pin.page_number, "expected_revision":pin.published_revision,
            "observation":observed, "status":status}


def confirmer_article(actor, site_id, base, token, *, page, parent=None, node=None, before=None):
    with transaction.atomic():
        site = _writing_site(actor, site_id)
        _current_head(site, base)
        presented = lire_observation(actor, site_id, token)
        if presented["status"] != "ok":
            raise SourceChanged(presented)
    fresh, profile = _read_page(actor, site_id, presented["page_number"], previous=presented)
    if fresh["status"] != "ok" or fresh["published_revision"] != presented["published_revision"]:
        raise SourceChanged(fresh)
    with transaction.atomic():
        site = _writing_site(actor, site_id)
        head = _current_head(site, base)
        link = _link(site.pk)
        obs = EditorialObservation.objects.filter(site=site, attempt=_uuid(fresh["token"])).first()
        if (not obs or _profile(link) != profile or link.instance_id != obs.instance_id
                or link.attempt_id != obs.connection_attempt):
            raise Conflict("L’observation a changé. Vérifiez à nouveau cet article.")
        pin, _ = EditorialReference.objects.get_or_create(site=site, instance_id=obs.instance_id,
            page_number=obs.page_number, published_revision=obs.published_revision)
        document = deepcopy(head.document)
        document["schema_version"] = 4
        target = _member(document["pages"], page)
        if node is not None:
            original = _block_location(target, node)[2]
            ref = original["definition"]
            manifest = definition(site.pk, ref["scope"], ref["key"], ref["version"])
            if not manifest or manifest["renderer"] != "article":
                raise ValidationError("Sélectionnez une occurrence d’article.")
            command = {"action": "block_edit", "id": node}
        else:
            standard = ComponentVersion.objects.filter(site=None, key="article", origin="standard",
                                                       renderer="article", retired=False).order_by("-version").first()
            if standard is None:
                raise ValidationError("Le composant Article Wagtail est indisponible.")
            ref = {"scope": "global", "key": standard.key, "version": standard.version}
            command = {"action": "block_add", "parent": parent, "before": before}
        command.update(definition=ref, props={"content": {"kind": "wagtail_content", "ref_id": str(pin.pk)}})
        selected = _apply(site.pk, target, command)
        checked = _check_document(document, site.pk, None, None, {}, head.document, preserve=True)
        return _save(actor, site, head, checked, {}, None,
                     editorial_binding=(page, selected, "content", str(pin.pk))), selected
