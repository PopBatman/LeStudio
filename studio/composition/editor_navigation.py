"""Choix du point d'entrée et reprise des signets de l'ancien atelier."""
from urllib.parse import urlencode

from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from registre import services as registry
from registre.views import require_manager, screen

from .canvas_format import canvas_format
from .services import lire_brouillon, lire_revision


def navigation_context(request):
    coexistence = settings.STUDIO_EDITOR_MODE == "coexistence"
    return {"editor_coexistence": coexistence,
            "studio_editor_route": "registre:site-editor" if coexistence else "registre:site-builder"}


def legacy(request, pk, canvas=False):
    if settings.STUDIO_EDITOR_MODE == "compatibility":
        return compatibility(request, pk)
    from .editor_views import editor
    return editor(request, pk, canvas=canvas)


def contains_block(blocks, identity):
    return any(block["id"] == identity or contains_block(block["children"], identity) for block in blocks)


@screen("GET", "HEAD", "POST")
def compatibility(request, pk):
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    url = reverse("registre:site-builder", args=[pk])
    submitted = request.method == "POST"
    if submitted or request.GET.get("action"):
        require_manager(request.user, site)
    source = request.POST if submitted else request.GET
    # A stale form returns to the current head and never replays the old command.
    revision_id = source.get("revision") if not submitted else None
    revision = (lire_revision(request.user, pk, revision_id) if revision_id
                else lire_brouillon(request.user, pk))
    pages = ((revision or {}).get("document") or {}).get("pages", [])
    page_id = source.get("page")
    page = next((p for p in pages if not page_id or p["id"] == page_id), None)
    params = {}
    missing = False
    if revision_id:
        params["revision"] = revision["id"]
    if page_id:
        if page:
            params["page"] = page["id"]
        else:
            missing = True
    if page:
        sections = [s for s in page["sections"] if not source.get("section") or s["id"] == source["section"]]
        if source.get("node") and any(contains_block(s["blocks"], source["node"]) for s in sections):
            params["selection"] = source["node"]
        elif source.get("section") and sections:
            params["selection"] = sections[0]["id"]
            missing = bool(source.get("node"))
        elif source.get("section") or source.get("node"):
            missing = True
    elif source.get("section") or source.get("node"):
        missing = True
    for key in ("format", "largeur"):
        if source.get(key):
            try:
                fmt, width = canvas_format({key: source[key]})
            except Http404:
                missing = True
            else:
                params[key] = fmt if key == "format" else width
    if not submitted and source.get("action"):
        params["edit"] = "1"
    target = url + ("?" + urlencode(params) if params else "")
    if submitted:
        return render(request, "composition/editor_resume.html", {
            "site": site, "target": target,
            "reason": "Ce formulaire provient de l’ancien atelier. Aucune modification enregistrée.",
        }, status=409)
    if missing:
        return render(request, "composition/editor_resume.html", {
            "site": site, "target": target,
            "reason": "Une cible du signet est introuvable ou son format est indisponible.",
        })
    return redirect(target)
