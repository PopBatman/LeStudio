"""Private, short-lived Wagtail preview receipts in the operator's Studio session."""
import hashlib
import json
import math
from datetime import timedelta
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from registre import services as registry
from registre.views import screen

from .models import CompositionRevision, PreviewTicket
from .preview import PreviewError, render_preview
from .services import lire_brouillon, lire_revision


LIFETIME = timedelta(minutes=10)
MAX_TICKETS_PER_OPERATOR = 12


def fingerprint(result):
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode()).hexdigest()


def destination(site, origin, page=None):
    if origin not in ("editor", "canvas"):
        return reverse("registre:site", args=[site.pk])
    route = origin if settings.STUDIO_EDITOR_MODE == "coexistence" else "builder"
    url = reverse("registre:site-" + route, args=[site.pk])
    return url + "?" + urlencode({"page": page}) if page else url


def lookup_page(document, identity):
    return next((p for p in (document or {}).get("pages", []) if p["id"] == identity), None)


def issue(request, revision, page, started, result):
    now = timezone.now()
    deadline = started + LIFETIME
    if now >= deadline:
        return None
    with transaction.atomic():
        get_user_model().objects.select_for_update().get(pk=request.user.pk)
        session = Session.objects.select_for_update().filter(
            pk=request.session.session_key, expire_date__gt=now).first()
        if session is None:
            raise Http404
        PreviewTicket.objects.filter(expires_at__lte=now).delete()
        active = PreviewTicket.objects.filter(operator=request.user).order_by("-created_at", "-pk")
        superseded = list(active.values_list("pk", flat=True)[MAX_TICKETS_PER_OPERATOR - 1:])
        if superseded:
            PreviewTicket.objects.filter(pk__in=superseded).delete()
        return PreviewTicket.objects.create(
            operator=request.user, session=session, revision_id=revision, page_id=page,
            fingerprint=fingerprint(result), created_at=started, expires_at=deadline)


def prepare_page(request, pk):
    """Read a page choice and, on explicit POST, prepare its private preview receipt."""
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    head = lire_brouillon(request.user, pk)
    submitted = request.method == "POST"
    params = request.POST if submitted else request.GET
    origin = params.get("origine", "")
    revision_id = params.get("revision")
    revision = lire_revision(request.user, pk, revision_id) if revision_id else head
    pages = (revision and revision["document"] or {}).get("pages", [])
    page_id = params.get("page") or (pages[0]["id"] if pages else "")
    page = lookup_page(revision and revision["document"], page_id)
    ctx = dict(site=site, head=head, revision=revision, pages=pages, page=page,
               revisions=CompositionRevision.objects.filter(site=site).order_by("-number").values("id", "number"),
               origin=origin, return_url=destination(site, origin, page_id if head and lookup_page(head["document"], page_id) else None))
    status = 200
    ticket = None
    if revision and revision["status"] != "ok":
        ctx["error"] = "Le format de cette révision est incompatible."
        status = 409
    elif not submitted and params.get("page") and page is None:
        ctx["error"] = "La page demandée est absente de cette révision. Choisissez une autre page."
    elif submitted and (not revision_id or not page or not params.get("page")):
        ctx["error"] = "Sélectionnez une page présente dans cette révision."
        status = 422
    elif submitted:
        started = timezone.now()
        try:
            result = render_preview(request.user, pk, revision_id, page_id)
        except PreviewError as error:
            ctx["error"] = str(error)
            status = 409
        else:
            ticket = issue(request, revision_id, page_id, started, result)
            if ticket is None:
                ctx["error"] = "La préparation a expiré. Vous pouvez la relancer."
                status = 410
    return ctx, status, ticket


@screen("GET", "HEAD", "POST")
def prepare(request, pk):
    ctx, status, ticket = prepare_page(request, pk)
    if ticket:
        origin = ctx["origin"]
        url = reverse("registre:preview-view", args=[pk, ticket.pk])
        return redirect(url + ("?" + urlencode({"origine": origin}) if origin in ("canvas", "editor") else ""))
    return render(request, "composition/preview_prepare.html", ctx, status=status)


def get_ticket(request, pk, ticket):
    return get_object_or_404(PreviewTicket.objects.select_related("revision", "revision__site"),
                             pk=ticket, operator=request.user, session_id=request.session.session_key,
                             revision__site_id=pk, revision__site__in=registry.sites(request.user))


def verified(request, ticket):
    """Repeat rights and dependency checks before each delivery, including HEAD."""
    if timezone.now() >= ticket.expires_at:
        return None, "Cet aperçu a expiré. Préparez à nouveau la révision.", 410
    try:
        result = render_preview(request.user, ticket.revision.site_id, str(ticket.revision_id), str(ticket.page_id))
    except PreviewError as error:
        return None, str(error), 409
    if fingerprint(result) != ticket.fingerprint:
        return None, "Le rendu ou ses ressources ont changé. Préparez à nouveau la révision.", 409
    if timezone.now() >= ticket.expires_at:
        return None, "Cet aperçu a expiré. Préparez à nouveau la révision.", 410
    if not PreviewTicket.objects.filter(pk=ticket.pk, revision__site__in=registry.sites(request.user)).exists():
        raise Http404
    return result, "", 200


def compare(current, previous, page):
    if not previous:
        return []
    if not previous.get("document"):
        return ["Le format de la révision précédente est incompatible."]
    old = lookup_page(previous["document"], page["id"])
    if not old:
        return ["Page ajoutée depuis la révision précédente."]
    changes = [label for key, label in (
        ("title", "Titre de page modifié."), ("slug", "Adresse de page modifiée."),
        ("parent_id", "Parent de la page modifié."), ("sections", "Composition de la page modifiée."),
    ) if old.get(key) != page.get(key)]
    for key, label in (("menus", "Navigation modifiée."), ("theme", "Apparence du site modifiée.")):
        if current.get(key) != previous["document"].get(key):
            changes.append(label)
    return changes or ["Composition identique pour cette page."]


@screen("GET", "HEAD")
def view(request, pk, ticket):
    receipt = get_ticket(request, pk, ticket)
    rev = receipt.revision
    head = lire_brouillon(request.user, pk)
    page_id = str(receipt.page_id)
    page = lookup_page(rev.document, page_id)
    if not page:
        raise Http404
    origin = request.GET.get("origine", "")
    parent = lire_revision(request.user, pk, rev.parent_id) if rev.parent_id else None
    head_has_page = bool(head and lookup_page(head["document"], page_id))
    result, error, code = verified(request, receipt)
    context = dict(site=rev.site, receipt=receipt, revision=rev, head=head, page=page, parent=parent,
                   previous_page=parent and lookup_page(parent["document"], page_id),
                   head_has_page=head_has_page, changes=compare(rev.document, parent, page),
                   manifest=result and result["manifest"], available=result is not None,
                   origin=origin, return_url=destination(rev.site, origin, page_id if head_has_page else None),
                   error=error, expires_ms=int(receipt.expires_at.timestamp()*1000))
    return render(request, "composition/preview_view.html", context, status=code)


@screen("GET", "HEAD")
def document(request, pk, ticket):
    receipt = get_ticket(request, pk, ticket)
    result, error, code = verified(request, receipt)
    content = result["html"] if result else format_html('<p lang="fr">{}</p>', error)
    response = HttpResponse(content, status=code, content_type="text/html; charset=utf-8")
    response["Content-Security-Policy"] = (
        "sandbox; default-src 'none'; style-src 'unsafe-inline'; img-src data:; font-src data:; "
        "frame-ancestors 'self'; form-action 'none'; base-uri 'none'")
    response["Referrer-Policy"] = "no-referrer"
    response["X-Content-Type-Options"] = "nosniff"
    if result:
        head = lire_brouillon(request.user, pk)
        response["X-Studio-Head"] = str(head["number"])
        response["Refresh"] = str(max(1, math.ceil((receipt.expires_at-timezone.now()).total_seconds())))
    return response


@screen("POST")
def close(request, pk, ticket):
    receipt = get_ticket(request, pk, ticket)
    head = lire_brouillon(request.user, pk)
    page = lookup_page(head and head["document"], str(receipt.page_id))
    url = destination(receipt.revision.site, request.POST.get("origine"), page and page["id"])
    receipt.delete()
    return redirect(url)
