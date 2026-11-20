from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from composition.models import CompositionRevision
from depots.services import latest_submission
from raccordement.services import LinkError, inspect_link
from workspace.access import is_operator

from . import services as svc
from .forms import ClientForm, ContactForm, SiteForm, VersionForm
from .models import Client
from .raccordement import connection_panel


def screen(*methods):
    def decorate(view):
        @never_cache
        @login_required
        @require_http_methods(methods)
        @wraps(view)
        def protected(request, *args, **kwargs):
            try:
                if not is_operator(request.user):
                    raise PermissionDenied
                return view(request, *args, **kwargs)
            except (Http404, PermissionDenied) as exc:
                code = 404 if isinstance(exc, Http404) else 403
                return render(request, "registre/error.html", {"code": code}, status=code)
        return protected
    return decorate


def page_of(request, queryset):
    return Paginator(queryset, 25).get_page(request.POST.get("page", 1))


@screen("GET", "HEAD", "POST")
def client_list(request):
    q = request.POST.get("q", "").strip()
    kind = request.POST.get("type", "")
    if "\x00" in q or len(q) > 160 or kind not in {"", *dict(Client.TYPES)}:
        return render(request, "registre/search_error.html", status=400)
    archived = request.GET.get("etat") == "archives"
    rows = svc.clients(request.user).filter(archived_at__isnull=not archived)
    if q:
        rows = rows.filter(display_name__icontains=q)
    if kind:
        rows = rows.filter(client_type=kind)
    return render(request, "registre/list.html", {
        "client_list": True, "title": "Clients", "archived": archived, "q": q, "kind": kind,
        "types": Client.TYPES, "create": svc.can_create_client(request.user),
        "page": page_of(request, rows.order_by("display_name", "pk")),
    })


@screen("GET", "HEAD", "POST")
def site_list(request):
    q = request.POST.get("q", "").strip()
    if "\x00" in q or len(q) > 253:
        return render(request, "registre/search_error.html", status=400)
    rows = svc.sites(request.user)
    if q:
        rows = rows.filter(Q(name__icontains=q) | Q(domain__icontains=q))
    return render(request, "registre/list.html", {
        "title": "Mes sites", "q": q, "page": page_of(request, rows.order_by("name", "pk")),
    })


@screen("GET", "HEAD")
def client_detail(request, pk):
    client = get_object_or_404(svc.clients(request.user), pk=pk)
    return render(request, "registre/client.html", {
        "client": client, "manage": svc.can_manage(request.user, client),
        "contacts": client.contacts.order_by("display_name", "pk"),
        "sites": svc.sites(request.user).filter(client=client).order_by("name", "pk"),
    })


@screen("GET", "HEAD")
def site_detail(request, pk):
    site = get_object_or_404(svc.sites(request.user), pk=pk)
    try:
        snapshot = inspect_link(request.user, site.pk)
    except LinkError:
        raise Http404 from None
    manage = svc.can_manage(request.user, site)
    return render(request, "registre/site.html", {
        "site": site, "manage": manage, "last_deposit": latest_submission(request.user, pk),
        "revision_number": CompositionRevision.objects.filter(site=site).order_by("-number").values_list("number", flat=True).first(),
        "connection": connection_panel(snapshot, site.pk, manage),
        "client": svc.clients(request.user).filter(pk=site.client_id).first(),
    })


def require_manager(user, obj):
    if not svc.can_manage(user, obj):
        raise PermissionDenied


def editable_client(user, pk):
    client = get_object_or_404(svc.clients(user), pk=pk)
    require_manager(user, client)
    if client.archived_at:
        raise PermissionDenied
    return client


def editor(request, form_class, title, cancel, save, destination, peers, key, obj=None):
    initial = {name: getattr(obj, name) for name in form_class.base_fields if obj and name != "version"}
    if obj:
        initial["version"] = obj.updated_at.isoformat()
    form = form_class(request.POST if request.method == "POST" else None, initial=initial)
    status = 200
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data.copy()
        version = data.pop("version")
        try:
            if {"client", "client_id"} & request.POST.keys():
                raise ValidationError("Le rattachement ne peut pas être modifié.")
            record = save(data, version)
        except ValidationError as error:
            if hasattr(error, "error_dict"):
                for field, errors in error.error_dict.items():
                    for detail in errors:
                        form.add_error(field if field in form.fields else None, detail)
            else:
                form.add_error(None, error)

        except svc.Conflict:
            form.add_error(None, "Cette fiche a changé. Rechargez-la avant de reprendre la modification.")
            status = 409
        else:
            duplicate = peers.exclude(pk=record.pk).filter(**{key + "__iexact": getattr(record, key)}).exists()
            return redirect(destination(record) + ("?resultat=homonyme" if duplicate else "?resultat=enregistre"))
    return render(request, "registre/form.html", {
        "title": title, "form": form, "cancel": cancel, "conflict": status == 409,
    }, status=status)


@screen("GET", "HEAD", "POST")
def client_form(request, pk=None):
    if pk:
        obj = editable_client(request.user, pk)
        def save(data, version):
            return svc.update_client(request.user, pk, data, version)
    else:
        if not svc.can_create_client(request.user):
            raise PermissionDenied
        obj = None
        def save(data, version):
            return svc.create_client(request.user, data)
    def destination(record):
        return reverse("registre:client", args=[record.pk])
    cancel = destination(obj) if obj else reverse("registre:clients")
    return editor(request, ClientForm, "Modifier le client" if obj else "Créer un client", cancel,
                  save, destination, svc.clients(request.user), "display_name", obj)


@screen("GET", "HEAD", "POST")
def contact_form(request, pk, child=None):
    client = editable_client(request.user, pk)
    obj = get_object_or_404(client.contacts, pk=child) if child else None
    url = reverse("registre:client", args=[pk])
    def save(data, version):
        return svc.save_contact(request.user, pk, data, contact_id=child, version=version)
    return editor(request, ContactForm, "Modifier le contact" if obj else "Ajouter un contact",
                  url, save, lambda record: url, client.contacts.all(), "display_name", obj)


@screen("GET", "HEAD", "POST")
def site_create(request, pk):
    client = editable_client(request.user, pk)
    def save(data, version):
        return svc.create_site(request.user, pk, data)
    return editor(request, SiteForm, "Créer un site", reverse("registre:client", args=[pk]), save,
                  lambda obj: reverse("registre:site", args=[obj.pk]),
                  svc.sites(request.user).filter(client=client), "name")


@screen("GET", "HEAD", "POST")
def site_edit(request, pk):
    obj = get_object_or_404(svc.sites(request.user), pk=pk)
    require_manager(request.user, obj)
    url = reverse("registre:site", args=[pk])
    def save(data, version):
        return svc.update_site(request.user, pk, data, version)
    return editor(request, SiteForm, "Modifier le site", url, save, lambda record: url,
                  svc.sites(request.user).filter(client_id=obj.client_id), "name", obj)


@screen("GET", "HEAD", "POST")
def archive(request, pk, archived):
    obj = get_object_or_404(svc.clients(request.user), pk=pk)
    require_manager(request.user, obj)
    form = VersionForm(request.POST if request.method == "POST" else None,
                       initial={"version": obj.updated_at.isoformat()})
    status = 200
    if request.method == "POST" and form.is_valid():
        try:
            svc.archive_client(request.user, pk, archived, form.cleaned_data["version"])
        except svc.Conflict:
            form.add_error(None, "La fiche a changé. Rechargez-la avant de confirmer.")
            status = 409
        else:
            result = "archive" if archived else "reactive"
            return redirect(reverse("registre:client", args=[pk]) + "?resultat=" + result)
    return render(request, "registre/archive.html", {
        "client": obj, "form": form, "archived": archived, "conflict": status == 409,
    }, status=status)
