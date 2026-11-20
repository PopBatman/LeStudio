from urllib.parse import urlencode

from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from registre import services as registry
from registre.views import require_manager, screen

from . import services
from .navigation import ImpactRequired, page_paths
from .navigation_forms import ACTIONS, FORMATS, EditForm, tree_rows


def selected(nodes, identity):
    if identity:
        for node in nodes:
            if node["id"] == identity:
                return node
        raise Http404
    return nodes[0] if nodes else None


def workshop(document, params, action):
    pages = tree_rows(document["pages"])
    paths = page_paths(document["pages"])
    menus = document["menus"]
    page = selected(pages, params.get("selection"))
    menu_id = params.get("menu_id") or params.get("menu")
    if action in {"menu_edit", "menu_delete"}:
        menu_id = params.get("id")
    menu = selected(menus, menu_id)
    items = tree_rows(menu["items"]) if menu else []
    effective_formats = {}
    for item in items:
        target = item["target"]
        item["destination"] = paths.get(target.get("page_id")) or target.get("url") or "Groupe sans lien"
        formats = set(item["visibility"])
        if item["parent_id"]:
            formats &= effective_formats[item["parent_id"]]
        effective_formats[item["id"]] = formats
        item["formats"] = ", ".join(label for key, label in FORMATS if key in formats) or "Masquée sur tous les formats"
    entity = action.partition("_")[0]
    editing = None
    if action and not action.endswith("_add"):
        if not params.get("id"):
            raise Http404
        editing = selected({"page": pages, "menu": menus, "item": items}[entity], params["id"])
        if entity == "page":
            page = editing
    if entity == "item" and not menu:
        raise Http404
    for row in pages:
        row["path"] = paths[row["id"]]
    references = [(m["label"], i["label"]) for m in menus for i in m["items"]
                  if i["target"].get("page_id") == page["id"]]
    return dict(pages=pages, page=page, menus=menus, menu=menu, items=items,
                references=references, editing=editing)


@screen("GET", "HEAD", "POST")
def navigation(request, pk, tab):
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    manage = registry.can_manage(request.user, site)
    post = request.method == "POST"
    params = request.POST if post else request.GET
    action = params.get("action", "")
    head = services.lire_brouillon(request.user, pk)
    ctx = dict(site=site, tab=tab, manage=manage, head=head, action=action)
    status = 200

    def response():
        return render(request, "composition/navigation.html", ctx, status=status)

    if post or action:
        require_manager(request.user, site)
    if action == "blank" and post:
        try:
            services.creer_brouillon(request.user, pk, {"kind": "blank"})
        except registry.Conflict as error:
            ctx["error"] = str(error)
            status = 409
            ctx["head"] = services.lire_brouillon(request.user, pk)
            if ctx["head"] and ctx["head"]["status"] == "ok":
                ctx.update(workshop(ctx["head"]["document"], {}, ""))
        else:
            return redirect(request.path + "?resultat=enregistre")
        return response()
    if not head or head["status"] != "ok":
        if post:
            status = 409
            ctx["error"] = "Le brouillon ne peut pas recevoir cette modification."
        return response()
    allowed = ("page_",) if tab == "pages" else ("menu_", "item_")
    if (action or post) and (action not in ACTIONS or not action.startswith(allowed)):
        raise Http404

    base = params.get("base") if post else head["id"]
    stale = post and base != head["id"]
    rebase = stale and params.get("relire") == "1"
    source = head
    if stale and not rebase:
        source = services.lire_revision(request.user, pk, base)
    if source["status"] != "ok":
        ctx["error"] = "Cette révision utilise un format incompatible."
        status = 409
        return response()
    try:
        ctx.update(workshop(source["document"], params, action))
    except Http404:
        if not rebase:
            raise
        ctx["error"] = "La sélection a disparu de la révision courante. Vous pouvez consulter votre proposition précédente."
        status = 409
        ctx.update(workshop(source["document"], {}, ""))
        ctx["previous"] = [(k, v) for k, v in params.items() if k in ("title", "slug", "label", "url", "parent_id", "before_id", "page_id")]
        ctx["action"] = ""
        return response()
    if not action:
        return response()

    editing, menu = ctx["editing"], ctx["menu"]
    form = EditForm(action, editing, ctx["pages"], ctx["items"], request.POST if post else None)
    if action == "page_add" and not post:
        form.initial["parent_id"] = ctx["page"]["id"]
    if action == "item_add" and not post:
        form.initial["parent_id"] = params.get("parent_id", "")
    if action.endswith("_move") and editing:
        siblings = [n["id"] for n in (ctx["pages"] if tab == "pages" else ctx["items"])
                    if n["parent_id"] == editing["parent_id"]]
        index = siblings.index(editing["id"])
        form.initial["before_id"] = next(iter(siblings[index + 1:]), "")
    ctx.update(form=form, base=head["id"] if rebase else base, action_title=ACTIONS[action])
    if not post:
        return response()
    resolutions = {key.removeprefix("resolution_"): val for key, val in params.items()
                   if key.startswith("resolution_") and val}
    if resolutions:
        pages = {row["id"]: row["path"] for row in ctx["pages"]}
        choices = {"remove": "Retirer l’entrée", "remove_branch": "Retirer la branche", **pages}
        ctx["previous_decisions"] = [
            (item["id"], item["label"], resolutions[item["id"]], choices.get(resolutions[item["id"]], "Cible indisponible"))
            for current_menu in ctx["menus"] for item in current_menu["items"] if item["id"] in resolutions
        ]
    if rebase:
        ctx["reloaded"] = True
        return response()
    if stale:
        ctx["conflict"] = True
        status = 409
        return response()
    if not form.is_valid():
        status = 422
        return response()
    command = form.command(action, editing and editing["id"], menu and menu["id"])
    try:
        saved = services.modifier_navigation(request.user, pk, base, command,
            confirmation=params.get("confirmation") or None, resolutions=resolutions)
    except ImpactRequired as error:
        if params.get("confirmation"):
            status = 409
            ctx["error"] = "Le bilan a changé. Examinez les conséquences avant de confirmer."
        ctx["impact"] = impact = error.impact
        removed_pages = {p["id"] for p in impact["pages"] if p["new_path"] is None}
        ctx["survivors"] = [p for p in ctx["pages"] if p["id"] not in removed_pages]
        for entry in impact["entries"]:
            entry["choice"] = resolutions.get(entry["id"])
        return response()
    except registry.Conflict:
        ctx["conflict"] = True
        status = 409
        return response()
    except ValidationError as error:
        ctx["error"] = " ".join(error.messages)
        status = 409 if getattr(error, "code", None) == "incompatible" else 422
        return response()
    query = {"resultat": "enregistre"}
    if tab == "pages" and action != "page_delete":
        if editing:
            query["selection"] = editing["id"]
        elif action == "page_add":
            previous = {p["id"] for p in ctx["pages"]}
            query["selection"] = next(p["id"] for p in saved["document"]["pages"] if p["id"] not in previous)
    if tab == "menus" and action != "menu_delete":
        if action == "menu_add":
            previous = {m["id"] for m in ctx["menus"]}
            query["menu"] = next(m["id"] for m in saved["document"]["menus"] if m["id"] not in previous)
        elif menu:
            query["menu"] = menu["id"]
    return redirect(reverse("registre:site-" + tab, args=[pk]) + "?" + urlencode(query))
