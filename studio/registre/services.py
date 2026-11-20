from datetime import datetime

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.http import Http404
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from workspace.access import is_operator
from .models import Client, ClientGrant, Contact, Site, SiteGrant


class Conflict(Exception):
    """An authorized change no longer matches the record's current state."""


def clients(user):
    if not is_operator(user):
        return Client.objects.none()
    return Client.objects.filter(grants__user=user)


def sites(user):
    if not is_operator(user):
        return Site.objects.none()
    return Site.objects.filter(grants__user=user)


def _creation_permission(user):
    return user.user_permissions.filter(
        content_type__app_label="registre", content_type__model="client", codename="create_client"
    )


def can_create_client(user):
    return is_operator(user) and _creation_permission(user).exists()


def can_manage(user, obj):
    return is_operator(user) and obj.grants.filter(user=user, level="manage").exists()


def _managed(queryset, user, pk):
    try:
        obj = queryset.select_for_update().get(pk=pk)
    except queryset.model.DoesNotExist:
        raise Http404 from None
    if not can_manage(user, obj):
        raise PermissionDenied
    return obj


def _check_version(obj, version):
    if not isinstance(version, datetime):
        try:
            version = parse_datetime(str(version))
        except ValueError:
            version = None
    if version != obj.updated_at:
        raise Conflict("La fiche a changé. Rechargez-la avant d’enregistrer.")


def _require_active(client):
    if client.archived_at:
        raise Conflict("Réactivez le client pour effectuer cette opération.")


def _save(obj, data, allowed):
    if set(data) - set(allowed):
        raise ValidationError("Le formulaire contient un champ non modifiable.")
    for field, value in data.items():
        if value is not None and not isinstance(value, str):
            raise ValidationError({field: "Saisissez du texte."})
        if value and "\x00" in value:
            raise ValidationError({field: "Le caractère nul est interdit."})
        setattr(obj, field, (value or "").strip())
    obj.full_clean()
    obj.save()
    return obj


CLIENT_FIELDS = ("client_type", "display_name")
SITE_FIELDS = ("name", "domain", "site_type", "description")
CONTACT_FIELDS = ("display_name", "role", "email", "phone")


@transaction.atomic
def create_client(user, data):
    if not is_operator(user) or not _creation_permission(user).select_for_update().exists():
        raise PermissionDenied
    obj = _save(Client(), data, CLIENT_FIELDS)
    ClientGrant.objects.create(user=user, client=obj, level="manage")
    return obj


@transaction.atomic
def update_client(user, client_id, data, version):
    obj = _managed(clients(user), user, client_id)
    _require_active(obj)
    _check_version(obj, version)
    return _save(obj, data, CLIENT_FIELDS)


@transaction.atomic
def archive_client(user, client_id, archived, version):
    obj = _managed(clients(user), user, client_id)
    if bool(obj.archived_at) == archived:
        return obj
    _check_version(obj, version)
    obj.archived_at = timezone.now() if archived else None
    obj.save(update_fields=["archived_at", "updated_at"])
    return obj


@transaction.atomic
def create_site(user, client_id, data):
    parent = _managed(clients(user), user, client_id)
    _require_active(parent)
    obj = _save(Site(client=parent), data, SITE_FIELDS)
    SiteGrant.objects.create(user=user, site=obj, level="manage")
    return obj


@transaction.atomic
def update_site(user, site_id, data, version):
    obj = _managed(sites(user), user, site_id)
    _check_version(obj, version)
    return _save(obj, data, SITE_FIELDS)


@transaction.atomic
def save_contact(user, client_id, data, contact_id=None, version=None):
    parent = _managed(clients(user), user, client_id)
    if contact_id is None:
        obj = Contact(client=parent)
    else:
        try:
            obj = parent.contacts.select_for_update().get(pk=contact_id)
        except Contact.DoesNotExist:
            raise Http404 from None
        _check_version(obj, version)
    _require_active(parent)
    return _save(obj, data, CONTACT_FIELDS)
