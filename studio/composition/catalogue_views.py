import re
from urllib.parse import urlencode

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from registre import services as registry
from registre.views import require_manager, screen

from . import appearance, catalogue
from .catalogue_forms import (AppearanceForm, BlockForm, PromotionForm, RemoveForm,
                              ReviewForm, THEME_KEYS, VARIANTS, ref, token_values)
from .appearance_contract import DEFAULTS
from .services import lire_brouillon

ORIGINS = {"standard": "Standard", "sur_mesure": "Sur mesure", "promotion_revue": "Promotion revue"}
DRAFT_ACTIONS = {"theme", "preference", "block", "remove", "clear_preference"}


def lookup(rows, identity):
    for row in rows:
        if row["id"] == identity:
            return row
    raise Http404


def sample_values(theme, definition, block):
    if definition and block:
        values = appearance.effective_appearance(theme, block, definition)
        theme = {**theme, **values["tokens"]}
        variant = values["variant"]
    else:
        variant = ""
    colors = {}
    for key, default in ((k, DEFAULTS[k]) for k in ("accent", "ink", "background")):
        color = theme.get(key, "")
        colors[key] = color if isinstance(color, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", color) else default
    gap = theme.get("gap", DEFAULTS["gap"])
    return {**colors, "gap": gap if type(gap) is int and 0 <= gap <= 128 else 16,
            "system_font": theme.get("font", DEFAULTS["font"]) == "system", "variant": variant}


@screen("GET", "HEAD")
def media(request, pk, asset):
    return HttpResponse(catalogue.media_png(request.user, pk, asset), content_type="image/png")


@screen("GET", "HEAD", "POST")
def library(request, pk, tab):
    return _library(request, pk, tab)


def _library(request, pk, tab, *, retry=True):
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    store = catalogue.bibliotheque(request.user, pk)
    head = lire_brouillon(request.user, pk)
    doc = head["document"] if head and head["status"] == "ok" else None
    theme = doc["theme"] if doc else {}
    post = request.method == "POST"
    params = request.POST if post else request.GET
    action = params.get("action", "theme" if tab == "appearance" else "")
    allowed = {"theme"} if tab == "appearance" else {"", "preference", "block", "remove", "propose", "review", "clear_preference"}
    if action not in allowed or (post and not action):
        raise Http404
    manage = registry.can_manage(request.user, site)
    if action == "review":
        if not store["can_review"]:
            raise PermissionDenied
    elif post or (action and tab == "catalogue"):
        require_manager(request.user, site)

    defs = store["definitions"]
    scope = params.get("scope", "")
    if action in {"block", "preference", "propose"} and not params.get("definition"):
        raise Http404
    if scope not in ("", "global", "site"):
        raise Http404
    visible = [d for d in defs if not scope or d["scope"] == scope]
    by_ref = {(d["scope"], d["key"], d["version"]): d for d in defs}
    block_id = params.get("block", "")
    definition_id = params.get("definition", "")
    blocks = []
    block = None
    pinned = None
    for page, b in appearance.occurrences(doc) if doc else ():
        definition = b["definition"]
        manifest = by_ref.get((definition["scope"], definition["key"], definition["version"]))
        blocks.append({"id": b["id"], "page": page["title"], "definition": definition,
                       "label": manifest["label"] if manifest else definition["key"]})
        if b["id"] == block_id:
            block, pinned = {**b, "page_id": page["id"]}, manifest
    chosen = lookup(defs, definition_id) if definition_id else pinned
    if action == "block" and any(d and d["renderer"] == "article" for d in (pinned, chosen)):
        raise Http404
    if chosen is None and not block and visible:
        chosen = visible[0]
    if block_id and not block and not post:
        raise Http404
    if chosen:
        chosen["origin_label"] = ORIGINS.get(chosen["origin"], chosen["origin"])
        chosen["variant_labels"] = [VARIANTS.get(v, v) for v in chosen["variants"]]
    reference = ref(chosen) if chosen else None
    pref = next((e for e in theme.get("components", []) if e["definition"] == reference), {})
    preview_block = (block if block and block["definition"] == reference else
                     {"definition": reference, "appearance": {}} if chosen else None)
    preview = sample_values(theme, chosen, preview_block if tab == "catalogue" else None)
    if tab == "appearance" or chosen and chosen["renderer"] == "image":
        current_media = (block or {}).get("props", {}).get("media") or theme.get("media") or {}
        preview["media"] = next((m for m in store["medias"] if isinstance(current_media, dict) and m["id"] == current_media.get("ref_id")), None)
        if tab != "appearance" and not preview["media"] and not block and store["medias"]:
            preview["media"] = store["medias"][0]
    ctx = dict(site=site, head=head, tab=tab, doc=doc, manage=manage, scope=scope, catalogue=visible,
               available=[d for d in defs if not d["retired"] and d["renderer"] != "article"], chosen=chosen, pinned=pinned, occurrence=block, blocks=blocks,
               promotions=store["promotions"], can_review=store["can_review"], action=action, preview=preview,
               medias=store["medias"], diagnostics=appearance.diagnostics(pk, doc) if doc else [],
               theme=theme, preference=pref, base=head["id"] if head else "")
    indexed_blocks = {b["id"]: b for b in blocks}
    for issue in ctx["diagnostics"]:
        issue["occurrence"] = indexed_blocks.get(issue["block_id"])
    ctx["blocked"] = any(row["blocking"] for row in ctx["diagnostics"])
    if post:
        ctx["submitted"] = [(k, v) for k, v in params.items() if
                            k in THEME_KEYS or k in ("variant", "definition", "confirmed") or k.startswith("prop_")]


    def show(status=200):
        return render(request, "composition/catalogue.html", ctx, status=status)
    if not action or action == "theme" and not doc and not post:
        return show()
    if action in DRAFT_ACTIONS and not doc:
        ctx["error"] = "Un brouillon compatible est nécessaire pour enregistrer."
        return show(409)
    data = request.POST if post else None
    if action in {"block", "remove"} and not block:
        if not post:
            raise Http404
        ctx["error"] = "Cette occurrence est absente de la révision courante."
        return show(409)
    if action in {"block", "preference", "propose"} and not chosen:
        raise Http404
    if action == "theme":
        form = AppearanceForm(action, None, store["medias"], theme, data)
    elif action == "preference":
        form = AppearanceForm(action, chosen, store["medias"], {**pref.get("tokens", {}), "variant": pref.get("variant")}, data)
    elif action == "block":
        form = BlockForm(chosen, store["medias"], block, pinned and pinned["renderer"] == chosen["renderer"], data)
    elif action == "clear_preference":
        reference = next((r["definition"] for r in ctx["diagnostics"] if r.get("definition") and
                          all(str(r["definition"][k]) == params.get("pref_" + k) for k in ("scope", "key", "version"))), None)
        if not reference:
            raise Http404
        ctx["unavailable_ref"] = reference
        form = RemoveForm(data=data)
        form.fields["confirmed"].label = "Confirmer la suppression de ce réglage de version"
    elif action == "remove":
        ctx["descendant_count"] = sum(1 for _ in walk_children(block))
        form = RemoveForm(data=data)
    elif action == "propose":
        if chosen["scope"] != "site" or chosen["retired"]:
            raise Http404
        form = PromotionForm(data=data)
    else:
        dossier = next((r for r in store["promotions"] if str(r.pk) == params.get("proposal")), None)
        if not dossier or dossier.author_id == request.user.pk:
            raise PermissionDenied
        ctx["dossier"] = dossier
        form = ReviewForm(data=data)
    ctx["form"] = form
    if not post:
        return show()
    if action in DRAFT_ACTIONS and params.get("base") != head["id"]:
        ctx["error"] = "Le brouillon a changé. Comparez la révision courante et votre proposition avant de la soumettre à nouveau."
        ctx["conflict"] = True
        ctx["current_values"] = form.initial
        return show(409)
    if not form.is_valid():
        return show(422)
    try:
        if action == "propose":
            catalogue.proposer(request.user, pk, chosen["id"], **form.cleaned_data)
        elif action == "review":
            values = dict(form.cleaned_data)
            approve = values.pop("decision") == "approve"
            catalogue.examiner(request.user, pk, dossier.pk, fingerprint=params.get("fingerprint", ""),
                               approve=approve, **values)
        else:
            if action == "clear_preference":
                command = {"action": "preference", "definition": reference, "appearance": {}}
            elif action == "theme":
                command = {"action": action, "values": token_values(THEME_KEYS, form.cleaned_data)}
            elif action == "preference":
                command = {"action": action, "definition": reference, "appearance": form.appearance()}
            elif action == "block":
                command = {"action": action, "id": block_id, "definition": reference,
                           "props": form.parameters(chosen["props"]), "appearance": form.appearance()}
            else:
                command = {"action": action, "id": block_id, "confirmed": form.cleaned_data["confirmed"]}
            appearance.modifier_apparence(request.user, pk, params["base"], command)
    except registry.Conflict as err:
        ctx["error"] = str(err)
        if action in DRAFT_ACTIONS and retry:
            # Recompute the scoped page and comparison with the head committed during this request.
            latest = lire_brouillon(request.user, pk)
            if latest and params.get("base") != latest["id"]:
                return _library(request, pk, tab, retry=False)
        return show(409)
    except ValidationError as err:
        ctx["error"] = " ".join(err.messages)
        return show(422)
    query = {"resultat": "enregistre"}
    if chosen and tab == "catalogue":
        query["definition"] = chosen["id"]
    if block_id and action != "remove":
        query["block"] = block_id
    return redirect(reverse("registre:site-" + tab, args=[pk]) + "?" + urlencode(query))


def walk_children(block):
    for child in block["children"]:
        yield child
        yield from walk_children(child)
