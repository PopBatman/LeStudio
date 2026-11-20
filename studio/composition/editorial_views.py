from urllib.parse import urlencode

from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from raccordement.services import editorial_admin_url
from registre import services as registry
from registre.views import require_manager, screen

from . import appearance, editorial, services
from .appearance_contract import AppearanceContract
from .editor_forms import ArticleForm
from .structure import block_rows


def targets_for(page, manifests):
    for number, section in enumerate(page["sections"], 1):
        label = f"Section {number}"
        yield {"id": section["id"], "label": label}
        for row in block_rows(section["blocks"], manifests, section["id"]):
            is_article = (row["pinned"] or {}).get("renderer") == "article"
            if is_article or row["is_container"]:
                yield {"id": row["id"], "label": f"{label} · {row['label']}",
                       "article": row if is_article else None}


@screen("GET", "HEAD", "POST")
def articles(request, pk):
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    post = request.method == "POST"
    if post:
        require_manager(request.user, site)
    params = request.POST if post else request.GET
    head = services.lire_brouillon(request.user, pk)
    revision = services.lire_revision(request.user, pk, params["revision"]) if params.get("revision") else head
    historical = bool(revision and revision["id"] != head["id"])
    ctx = {"site": site, "revision": revision, "historical": historical,
           "manage": registry.can_manage(request.user, site) and not historical}

    def show(status=200):
        return render(request, "composition/editorial.html", ctx, status=status)

    builder = reverse("registre:site-builder", args=[pk])
    ctx["return_url"] = builder
    if not revision or revision["status"] != "ok":
        return show(409 if post else 200)
    if post and (historical or params.get("base") != head["id"]):
        ctx["error"] = "Le brouillon a changé. Relisez la sélection avant de vérifier la source."
        ctx["reload_url"] = request.path + "?" + urlencode({
            "page": params.get("page", ""), "selection": params.get("selection", "")})
        return show(409)
    doc = revision["document"]
    pages = doc["pages"]
    page = next((page for page in pages if page["id"] == params.get("page")), None) if params.get("page") else pages[0]
    if not page or (post and not params.get("page")):
        raise Http404
    history = {"revision": revision["id"]} if historical else {}
    coordinates = {"page": page["id"], **history}
    targets = list(targets_for(page, AppearanceContract(pk).manifests))
    target = next((row for row in targets if row["id"] == params.get("selection")), None)
    if (params.get("selection") or post) and not target:
        raise Http404
    ctx.update(pages=pages, page=page, targets=targets, target=target,
               diagnostics=appearance.diagnostics(pk, doc))
    if target:
        coordinates["selection"] = target["id"]
    ctx["return_url"] = builder + "?" + urlencode({**coordinates, **({"edit": 1} if ctx["manage"] else {})})
    if not target:
        return show()
    node = target.get("article")
    article = editorial.article_occurrence(request.user, pk, node) if node else {}
    ctx.update(article=article, action="article_reference")
    if ctx["manage"]:
        ctx["admin_url"] = editorial_admin_url(request.user, site)
        ctx["form"] = ArticleForm(data=params if post else None, initial={"page_number": article.get("page_number")})
    if not post:
        return show()
    try:
        if params.get("intent") == "verify":
            form = ctx["form"]
            if not form.is_valid():
                return show(422)
            ctx["proposal"] = editorial.verifier_article(request.user, pk, form.cleaned_data["page_number"])
        elif params.get("intent") == "confirm":
            _, identity = editorial.confirmer_article(request.user, pk, head["id"], params.get("observation"),
                page=page["id"], node=node["id"] if node else None, parent=None if node else target["id"])
            return redirect(builder + "?" + urlencode({"page": page["id"], "selection": identity, "edit": 1}))
        else:
            raise Http404
    except editorial.SourceChanged as exc:
        ctx.update(proposal=exc.observation, error=str(exc))
        return show(409)
    except registry.Conflict as exc:
        ctx["error"] = str(exc)
        return show(409)
    except ValidationError as exc:
        ctx["error"] = " ".join(exc.messages)
        return show(422)
    return show()
