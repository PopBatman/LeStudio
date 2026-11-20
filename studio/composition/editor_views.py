from urllib.parse import urlencode

from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from registre import services as registry
from registre.views import require_manager, screen

from raccordement.services import editorial_admin_url

from . import appearance, catalogue, editorial, services
from .appearance_contract import definition_key
from .canvas_forms import CanvasForm, setting_labels, settings
from .canvas_format import FORMATS, canvas_format
from .canvas_views import surface
from .catalogue_forms import PARAMETERS
from .editor import creer_atelier, modifier_structure
from .editor_forms import ACTIONS, ArticleForm, command, editor_form
from .navigation import page_paths
from .navigation_forms import tree_rows
from .structure import block_rows, indexed


def lookup(rows, identity):
    for row in rows:
        if row["id"] == identity:
            return row
    raise Http404


def structure(document, params, manifests, *, follow_node=False):
    pages = tree_rows(document["pages"])
    paths = page_paths(pages)
    for row in pages:
        row["path"] = paths[row["id"]]
    page = lookup(pages, params["page"]) if params.get("page") else pages[0]
    sections = [{**s, "label": f'Section {s["index"]}',
                 "rows": list(block_rows(s["blocks"], manifests, s["id"]))}
                for s in indexed(page["sections"])]
    section_id = params.get("section")
    if follow_node and params.get("node"):
        section_id = next((s["id"] for s in sections if any(
            row["id"] == params["node"] for row in s["rows"])), section_id)
    section = lookup(sections, section_id) if section_id else None
    node = None
    if params.get("node"):
        if not section:
            raise Http404
        node = lookup(section["rows"], params["node"])
    return dict(pages=pages, page=page, page_id=page["id"], sections=sections, section=section,
                section_id=section["id"] if section else "", occurrence=node, node_id=node["id"] if node else "")


def selected_values(ctx):
    node, section = ctx["occurrence"], ctx["section"]
    if not section:
        return []
    if not node:
        return [("Position", section["index"]), *layout_values(section["layout"])]
    props = []
    for key, value in node["props"].items():
        if key == "content" and (node["pinned"] or {}).get("renderer") == "article":
            continue
        if isinstance(value, dict) and value.get("kind") == "wagtail_content":
            props.append(("Référence éditoriale", "À vérifier"))
            continue
        if key == "layout" and node["is_container"]:
            props.extend(layout_values(value))
        elif key == "media" and isinstance(value, dict) and value.get("kind") == "media":
            props.append(("Image", next((m["label"] for m in ctx["medias"] if m["id"] == value["ref_id"]), "Indisponible")))
        else:
            props.append((PARAMETERS.get(key, key), value))
    parent = section if node["parent_id"] == section["id"] else lookup(section["rows"], node["parent_id"])
    style = node.get("appearance", {})
    props.extend((k, v) for k, v in style.get("tokens", {}).items() if not isinstance(v, dict))
    return [("Parent", parent["label"]), ("Position", node["index"]), *props,
            ("Variante", style.get("variant", "Hériter"))]


def layout_values(layout):
    labels = {"base": "Bureau", "tablet": "Tablette", "mobile": "Mobile"}
    keys = {"display": "disposition", "columns": "colonnes", "gap": "espacement"}
    displays = {"stack": "Pile", "grid": "Grille"}
    return [(f"{labels[screen]} · {keys[key]}", displays.get(value, value)) for screen, rules in layout.items()
            for key, value in rules.items()]


def inspector(ctx, params, data=None):
    action, section, node = ctx["action"], ctx["section"], ctx["occurrence"]
    needs_section = action and action != "section_add"
    needs_node = action.startswith("block_") and action != "block_add"
    if (needs_section and not section) or (needs_node and not node):
        raise Http404
    if action == "parent_layout" and node and not node["is_container"]:
        raise Http404
    pinned = node["pinned"] if node else None
    chosen = pinned if action != "block_add" else None
    if params.get("definition") and (not pinned or params["definition"] != pinned["id"] or action == "block_add"):
        chosen = lookup(ctx["definitions"], params["definition"])
    ctx.update(chosen=chosen, pinned=pinned, current_values=selected_values(ctx))
    article = pinned and pinned["renderer"] == "article"
    if action == "article_reference" and node and not (article or node["is_container"]):
        raise Http404
    if article and action == "block_edit":
        raise Http404
    ctx["article"] = None
    if article:
        ctx["article"] = editorial.article_occurrence(ctx["actor"], ctx["site"].pk, node)
    if ctx["manage"] and (article or action == "article_reference"):
        ctx["admin_url"] = editorial_admin_url(ctx["actor"], ctx["site"])
    if node:
        ctx["descendants"] = sum(1 for _ in block_rows(node["children"], {}, node["id"]))
    elif section:
        ctx["descendants"] = len(section["rows"])
        ctx["section_has_article"] = any((row["pinned"] or {}).get("renderer") == "article"
                                         for row in section["rows"])
    if action in ("block_add", "block_move"):
        ctx["sibling_parents"] = {row["id"]: row["parent_id"] for s in ctx["sections"] for row in s["rows"]}
    if node:
        ctx["current_values"] += setting_labels(*settings(ctx, "block_place"), ctx["format"])
    if section and (not node or node["is_container"]) and action == "parent_layout":
        ctx["current_values"] += setting_labels(*settings(ctx, action), ctx["format"])
    if action == "article_reference":
        ctx.update(title=ACTIONS[action], form=ArticleForm(data=data, initial={
            "page_number": (ctx["article"] or {}).get("page_number")
        }))
        if not data and params.get("comparer") == "1" and ctx["article"]:
            ctx["proposal"] = ctx["article"]["observation"]
    elif action in ("block_place", "parent_layout"):
        ctx.update(title=ACTIONS[action], form=CanvasForm(ctx, data))
    elif action:
        ctx.update(title=ACTIONS[action], form=editor_form(ctx, data))


def selection_after(envelope, page_id, identity):
    params = {"page": page_id, "resultat": "enregistre"}
    if identity:
        page = lookup(envelope["document"]["pages"], page_id)
        for section in page["sections"]:
            if str(identity) == section["id"]:
                return {**params, "section": section["id"]}
            if any(b["id"] == str(identity) for b in block_rows(section["blocks"], {}, section["id"])):
                return {**params, "section": section["id"], "node": str(identity)}
    return params


@screen("GET", "HEAD", "POST")
def editor(request, pk, canvas=False):
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    post = request.method == "POST"
    params = request.POST if post else request.GET
    action = params.get("action", "")
    if action or post:
        require_manager(request.user, site)
    head = services.lire_brouillon(request.user, pk)
    fmt, width = canvas_format(params)
    ctx = dict(site=site, actor=request.user, head=head, manage=registry.can_manage(request.user, site), action=action,
               canvas=canvas, format=fmt, format_label=FORMATS[fmt][0], canvas_width=width,
               custom_width=width if params.get("largeur") else None)

    def show(status=200):
        if canvas and "sections" in ctx and ctx["head"]["status"] == "ok":
            ctx["canvas_sections"] = surface(ctx)
        return render(request, "composition/editor.html", ctx, status=status)

    if action == "create" and post:
        try:
            creer_atelier(request.user, pk, params.get("origin"))
        except ValidationError as exc:
            ctx["error"] = " ".join(exc.messages)
            return show(422)
        except registry.Conflict as exc:
            ctx.update(error=str(exc), action="", head=services.lire_brouillon(request.user, pk))
            head = ctx["head"]
            creation_conflict = True
        else:
            return redirect(request.path + "?resultat=enregistre")
    else:
        if action not in {"", *ACTIONS} or post and not action:
            raise Http404
        creation_conflict = False
    if not head or head["status"] != "ok":
        return show(409 if post else 200)
    store = catalogue.bibliotheque(request.user, pk)
    manifests = {definition_key(d): d for d in store["definitions"]}
    ctx.update(definitions=[d for d in store["definitions"] if not d["retired"] and d["renderer"] != "article"], medias=store["medias"],
               base=head["id"], diagnostics=appearance.diagnostics(pk, head["document"]))
    if creation_conflict:
        ctx.update(structure(head["document"], {}, manifests))
        return show(409)
    base = params.get("base") if post else head["id"]

    def compare(latest):
        previous = services.lire_revision(request.user, pk, base)
        if previous["status"] != "ok" or latest["status"] != "ok":
            ctx.update(head=latest, error="Cette révision est incompatible.")
            return show(409)
        # Resolve the original selection in its authorised site before displaying any proposal.
        old = structure(previous["document"], params, manifests)
        ctx.update(old)
        inspector(ctx, params, params)
        proposal_form = ctx["form"]
        submitted = []
        for name, field in (proposal_form.fields.items() if proposal_form else ()):
            value = params.get(name)
            if value:
                choices = getattr(field, "choices", ())
                submitted.append((field.label, dict(choices).get(value, value)))
        ctx.update(head=latest, base=base, conflict=True, submitted=submitted,
                   diagnostics=appearance.diagnostics(pk, latest["document"]))
        try:
            ctx.update(structure(latest["document"], params, manifests, follow_node=bool(old["occurrence"])))
        except Http404:
            ctx.update(missing=True, form=None, action="", error="La sélection a disparu de la révision courante.")
            fallback = {"page": old["page_id"], "section": old["section_id"]}
            if old["occurrence"] and old["occurrence"]["parent_id"] != old["section_id"]:
                fallback["node"] = old["occurrence"]["parent_id"]
            for key in ("node", "section", "page", None):
                try:
                    ctx.update(structure(latest["document"], fallback, manifests))
                    break
                except Http404:
                    if key:
                        fallback.pop(key, None)
            inspector(ctx, {}, None)
            return show(409)
        inspector(ctx, params, params)
        if action == "article_reference" and params.get("observation"):
            try:
                ctx["proposal"] = editorial.lire_observation(request.user, pk, params["observation"])
            except Http404:
                ctx["error"] = "Cette vérification a expiré. Relisez le brouillon, puis vérifiez la source."
        if params.get("relire") == "1":
            ctx.update(base=latest["id"], reloaded=True, conflict=False)
            return show()
        # Re-reading uses the original selection and base. Only confirmation uses its new location.
        ctx["section_id"] = old["section_id"]
        return show(409)

    if post and not params.get("page"):
        raise Http404
    if post and base != head["id"]:
        return compare(head)
    ctx.update(structure(head["document"], params, manifests))
    inspector(ctx, params, request.POST if post else None)
    if not post or params.get("relire") == "1":
        return show()
    form = ctx["form"]
    if form is None:
        ctx["error"] = "Choisissez une version disponible pour ce site."
        return show(422)
    if action == "article_reference" and params.get("intent") == "confirm":
        try:
            saved, identity = editorial.confirmer_article(
                request.user, pk, base, params.get("observation"), page=ctx["page_id"],
                node=ctx["node_id"] if ctx["article"] else None,
                parent=None if ctx["article"] else ctx["node_id"] or ctx["section_id"])
        except editorial.SourceChanged as exc:
            ctx.update(proposal=exc.observation, error="La source a changé. Relisez le résultat avant de confirmer.")
            return show(409)
        except ValidationError as exc:
            ctx["error"] = " ".join(exc.messages)
            return show(422)
        except registry.Conflict as exc:
            latest = services.lire_brouillon(request.user, pk)
            if latest["id"] != base:
                return compare(latest)
            ctx["error"] = str(exc)
            return show(409)
        return saved_response(request, ctx, saved, identity)
    if not form.is_valid():
        return show(422)
    if action == "article_reference":
        if params.get("intent") != "verify":
            raise Http404
        try:
            ctx["proposal"] = editorial.verifier_article(request.user, pk, form.cleaned_data["page_number"])
        except ValidationError as exc:
            form.add_error(None, " ".join(exc.messages))
            return show(422)
        except registry.Conflict as exc:
            ctx["error"] = str(exc)
            return show(409)
        return show()
    if action in ("block_move", "block_add") and form.cleaned_data["before"]:
        before = form.cleaned_data["before"]
        target = next(row for section in ctx["sections"] for row in section["rows"] if row["id"] == before)
        if target["parent_id"] != form.cleaned_data["parent"]:
            form.add_error("before", "Choisissez un bloc appartenant à la destination.")
            return show(422)
    try:
        mutation = form.command(ctx) if isinstance(form, CanvasForm) else command(ctx)
        saved, identity = modifier_structure(request.user, pk, base, mutation)
    except ValidationError as exc:
        if isinstance(form, CanvasForm):
            form.add_domain_error(exc, ctx)
        else:
            form.add_error(None, " ".join(exc.messages))
        return show(422)
    except registry.Conflict:
        return compare(services.lire_brouillon(request.user, pk))
    return saved_response(request, ctx, saved, identity)


def saved_response(request, ctx, saved, identity):
    selection = selection_after(saved, ctx["page_id"], identity)
    selection["format"] = ctx["format"]
    if ctx["custom_width"]:
        selection["largeur"] = ctx["custom_width"]
    return redirect(request.path + "?" + urlencode(selection))
