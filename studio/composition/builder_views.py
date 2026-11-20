"""Canvas de consultation d'une révision rendue par le moteur raccordé."""
from base64 import b64encode
from functools import lru_cache
from hashlib import sha256
from math import ceil
import json
from urllib.parse import urlencode

from django.conf import settings
from django.core.exceptions import RequestDataTooBig, ValidationError
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from depots.provenance import is_imported_page
from registre import services as registry
from registre.views import screen

from . import preview_views as preview
from .appearance_contract import AppearanceContract
from .builder_batch import save_batch
from .canvas_format import canvas_format
from .catalogue import bibliotheque
from .editor import creer_atelier
from .structure import block_rows
from .models import BuilderSave, CompositionRevision
from .services import lire_brouillon, lire_revision
from .validation import MAX_BYTES


FRAME_END = "</body></html>"
INCOMPATIBLE = "La structure de ce rendu ne permet pas la sélection dans le canvas."


def layers_for(site, page):
    if not page:
        return []
    manifests = AppearanceContract(site.pk).manifests
    return [
        {"id": row["id"], "label": row["label"], "summary": row["summary"],
         "depth": row["depth"], "parent_id": row["parent_id"], "container": row["is_container"],
         "renderer": (row["pinned"] or {}).get("renderer", ""), "key": row["definition"]["key"],
         "version": row["definition"]["version"]}
        for section in page["sections"]
        for row in block_rows(section["blocks"], manifests, section["id"])
    ]


def render_shell(request, context, status):
    context["layers"] = layers_for(context["site"], context["page"])
    site, revision, page = context["site"], context["revision"], context["page"]
    params = request.POST if request.method == "POST" else request.GET
    if params.get("saved") == "1" and revision:
        context["just_saved"] = BuilderSave.objects.filter(
            site=site, operator=request.user, revision_id=revision["id"]
        ).exists()
    selected = params.get("selection", "")[:36]
    section = next((s for s in (page or {}).get("sections", []) if s["id"] == selected), None)
    layer = next((row for row in context["layers"] if row["id"] == selected), None)
    context.update(initial_selection=selected, selected_section=section,
                   missing_selection=bool(selected and not section and not layer))
    fmt, width = canvas_format(params)
    context["initial_width"] = width if params.get("largeur") or "format" in params else None
    context["may_manage"] = registry.can_manage(request.user, site)
    if (request.method != "HEAD" and context["may_manage"] and revision and page
            and is_imported_page(site.pk, revision["id"], page["id"])):
        url = reverse("registre:figma-compare", args=[site.pk, revision["id"], page["id"]])
        receipt = context.get("receipt")
        context["comparison_url"] = url + ("?" + urlencode({"ticket": receipt.pk}) if receipt else "")
    if (request.method != "HEAD" and context["may_manage"] and revision and page
            and revision["id"] == context["head"]["id"] and revision["status"] == "ok"
            and not context.get("structure_only")):
        library = bibliotheque(request.user, site.pk)
        endpoint = reverse("registre:builder-save", args=[site.pk])
        context["builder_edit"] = {
            "page": page, "revision": revision["id"], "number": revision["number"],
            "open_editor": request.GET.get("edit") == "1", "selection": selected,
            "width": width, "format": fmt,
            "definitions": library["definitions"], "theme": revision["document"]["theme"],
            "medias": [{**media, "url": reverse("registre:site-media", args=[site.pk, media["id"]])}
                       for media in library["medias"]],
            "catalogue_url": reverse("registre:site-catalogue", args=[site.pk]),
            "articles_url": reverse("registre:site-articles", args=[site.pk]),
            "save_url": endpoint, "access_url": endpoint,
            "prepare_url": reverse("registre:site-builder", args=[site.pk]),
        }
        context["initial_palette"] = [d for d in library["definitions"]
                                      if not d["retired"] and d["renderer"] in
                                      {"heading", "text", "image", "button", "container", "signature"}
                                      and (d["renderer"] != "image" or library["medias"])]
    return render(request, "composition/builder.html", context, status=status)


@screen("GET", "HEAD", "POST")
def prepare(request, pk):
    if request.method == "POST" and request.POST.get("start") in ("blank", "template"):
        try:
            creer_atelier(request.user, pk, request.POST["start"])
        except registry.Conflict:
            # A repeated first-open should return the existing head.
            pass
        return redirect("registre:site-builder", pk)
    context, status, ticket = preview.prepare_page(request, pk)
    if ticket:
        url = reverse("registre:builder-view", args=[pk, ticket.pk])
        options = {k: request.POST[k][:36] for k in ("selection", "largeur", "format") if request.POST.get(k)}
        if request.POST.get("saved") == "1":
            options["saved"] = "1"
        if options:
            url += "?" + urlencode(options)
        return redirect(url)
    # The POST to the engine could have overlapped a change of mandate.
    if request.method == "POST":
        context["head"] = lire_brouillon(request.user, pk)
    page, head = context["page"], context["head"]
    context.update(available=False, structure_only=request.GET.get("mode") == "structure",
                   head_has_page=bool(page and head and preview.lookup_page(head["document"], page["id"])))
    return render_shell(request, context, status)


def canvas_result(request, receipt):
    result, error, code = preview.verified(request, receipt)
    if result is None:
        # A lost mandate or session during a failed render must close the entire
        # workspace, even when the transport reports only a rendering error.
        preview.get_ticket(request, receipt.revision.site_id, receipt.pk)
        return None, error, code
    if not (result["html"].startswith('<!doctype html>\n<html lang="fr"><head>')
            and result["html"].rstrip().endswith(FRAME_END)
            and result["html"].count(FRAME_END) == 1):
        return None, INCOMPATIBLE, 409
    return result, error, code


@screen("GET", "HEAD")
def view(request, pk, ticket):
    receipt = preview.get_ticket(request, pk, ticket)
    result, error, code = canvas_result(request, receipt)
    revision = lire_revision(request.user, pk, receipt.revision_id)
    page = preview.lookup_page(revision["document"], str(receipt.page_id))
    if page is None:
        raise Http404
    head = lire_brouillon(request.user, pk)
    context = {
        "site": receipt.revision.site, "receipt": receipt, "head": head, "revision": revision,
        "pages": revision["document"]["pages"], "page": page,
        "revisions": CompositionRevision.objects.filter(site_id=pk).order_by("-number").values("id", "number"),
        "initial_selection": request.GET.get("selection", "")[:36],
        "available": result is not None, "manifest": result and result["manifest"],
        "head_has_page": preview.lookup_page(head["document"], page["id"]) is not None,
        "expires_ms": int(receipt.expires_at.timestamp() * 1000), "error": error,
    }
    return render_shell(request, context, code)


@lru_cache(maxsize=1)
def frame_module():
    # Only this static module packaged with Studio may execute in the opaque frame.
    script = (settings.BASE_DIR / "static/ui/builder-frame.js").read_text(encoding="utf-8")
    digest = b64encode(sha256(script.encode("utf-8")).digest()).decode("ascii")
    return script, digest


@screen("GET", "HEAD")
def document(request, pk, ticket):
    receipt = preview.get_ticket(request, pk, ticket)
    result, error, code = canvas_result(request, receipt)
    script_policy = "sandbox; script-src 'none';"
    if result:
        head = lire_brouillon(request.user, pk)
        script, digest = frame_module()
        script_policy = f"sandbox allow-scripts; script-src 'sha256-{digest}';"
        tag = format_html(
            '<script data-instance="{}" data-revision="{}" data-page="{}" data-fingerprint="{}">{}</script>',
            result["manifest"]["instance_id"], receipt.revision_id, receipt.page_id,
            receipt.fingerprint, mark_safe(script),
        )
        # The original HTML was validated by FEAT-004 and checked for the exact
        # renderer envelope above. Do not parse and reserialize its contents.
        content = result["html"].replace(FRAME_END, str(tag) + FRAME_END)
    else:
        content = format_html('<p lang="fr">{}</p>', error)
    response = HttpResponse(content, status=code, content_type="text/html; charset=utf-8")
    response["Content-Security-Policy"] = (
        f"{script_policy} default-src 'none'; style-src 'unsafe-inline'; img-src data:; font-src data:; "
        "connect-src 'none'; frame-ancestors 'self'; form-action 'none'; base-uri 'none'")
    response["Referrer-Policy"] = "no-referrer"
    response["X-Content-Type-Options"] = "nosniff"
    if result:
        response["Refresh"] = str(max(1, ceil((receipt.expires_at - timezone.now()).total_seconds())))
        response["X-Studio-Head"] = str(head["number"])
        response["X-Studio-Head-Has-Page"] = "1" if preview.lookup_page(head["document"], str(receipt.page_id)) else "0"
    return response


@screen("HEAD", "POST")
def save(request, pk):

    site = get_object_or_404(registry.sites(request.user), pk=pk)
    if not registry.can_manage(request.user, site):
        return JsonResponse({"code": "readonly", "error": "La gestion du site est requise."}, status=403)
    if request.method == "HEAD":
        return HttpResponse(status=204)
    if request.content_type != "application/json":
        return JsonResponse({"code": "format", "error": "Le corps JSON est requis."}, status=415)
    try:
        body = request.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise RequestDataTooBig()
        data = json.loads(body)
        if not isinstance(data, dict):
            raise ValueError
    except RequestDataTooBig:
        return JsonResponse({"code": "size", "error": "La sauvegarde dépasse la taille autorisée."}, status=413)
    except (ValueError, RecursionError):
        return JsonResponse({"code": "format", "error": "Le lot de commandes est illisible."}, status=400)
    try:
        return JsonResponse(save_batch(request.user, site.pk, data))
    except registry.Conflict as exc:
        return JsonResponse({"code": "conflict", "error": str(exc)}, status=409)
    except ValidationError as exc:
        code = getattr(exc, "code", None) or "invalid"
        return JsonResponse({"code": code, "error": " ".join(exc.messages)},
                            status=409 if code == "key_reused" else 422)
