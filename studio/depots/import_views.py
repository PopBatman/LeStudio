from urllib.parse import urlencode

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.debug import sensitive_post_parameters

from composition.catalogue import bibliotheque
from composition.services import lire_brouillon
from registre import services as registry
from registre.views import require_manager, screen

from . import imports, services
from .models import ImportAnalysis
from .provenance import result_pages
from .import_forms import DecisionForm, DestinationForm, FORMATS


def review_rows(analysis):
    return [{**row, "decision": analysis.decisions.get(row["id"], {})} for row in analysis.proposals]


def destinations(analysis, pages, data=None):
    previous = {row["frame_id"]: row for row in analysis.destinations}
    return [(frame, DestinationForm(frame, previous.get(frame["id"], {}), pages, index, data=data))
            for index, frame in enumerate(analysis.observation["frames"])]


def edit_context(ctx, node_id, data, actor, requested_definition):
    a = ctx["analysis"]
    prop = next((row for row in a.proposals if row["id"] == node_id), None)
    if prop is None:
        raise Http404
    previous = a.decisions.get(node_id, {})
    selected = requested_definition or previous.get("definition") or prop.get("suggested")
    candidate = next((c for c in prop["candidates"] if str(c["id"]) == str(selected)), None)
    form = DecisionForm(prop, candidate, previous, bibliotheque(actor, ctx["site"].pk)["medias"], data=data)
    frame = next(f for f in a.observation["frames"] if f["id"] == prop["frame_id"])
    ctx.update(node=prop, candidate=candidate, decision_form=form, frame=frame)
    return form


def review_context(ctx, request):
    a = ctx["analysis"]
    head = lire_brouillon(request.user, ctx["site"].pk)
    pages = (head and head["document"] or {}).get("pages", [])
    rows = review_rows(a)
    ctx.update(pages=pages, head=head, review_page=Paginator(rows, 30).get_page(request.GET.get("p")),
               accepted=sum(r['decision'].get("action") in ("accept", "correct") for r in rows),
               excluded=sum(r['decision'].get("action") == "exclude" for r in rows),
               missing=sum(not r['decision'] for r in rows))
    if ctx['screen'] == "destinations":
        ctx['frame_forms'] = destinations(a, pages, request.POST if request.method == "POST" else None)
    elif ctx['screen'] == "node":
        post = request.POST if request.method == "POST" else None
        edit_context(ctx, request.GET.get("node") or request.POST.get("node"), post, request.user,
                     (post or request.GET).get("definition"))
    elif ctx['screen'] == "summary":
        names = {f['id']: f['name'] for f in a.observation['frames']}
        by_group = {}
        for row in a.destinations:
            by_group.setdefault(row['group'], set()).add(row['format'])
        ctx["dest_rows"] = [{**row, "frame": names.get(row["frame_id"]),
                             "parent": next((p["title"] for p in pages if p["id"] == row.get("parent_id")), ""),
                             "format_label": dict(FORMATS).get(row['format']),
                             "absent": [label for key, label in FORMATS if key not in by_group[row["group"]]]}
                            for row in a.destinations]


@screen("GET", "HEAD", "POST")
@sensitive_post_parameters()
def review(request, pk, submission_id):
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    require_manager(request.user, site)
    row = services.submission_for(request.user, pk, submission_id)
    args = (request.user, pk, submission_id)
    post = request.method == "POST"
    params = request.POST if post else request.GET
    ctx = {"site": site, "row": row, "screen": params.get("screen", "review"), "analysis": None}
    status = 200
    try:
        action = params.get("action") if post else None
        if action == "start":
            imports.start(*args)
            return redirect(request.path)
        if action == "confirm" and ctx["screen"] == "summary":
            result = imports.confirm(*args, params.get("token", ""))
            # A replay has only the durable receipt, even if Figma is offline.
            ctx.update(analysis=result, imported_pages=result_pages(result))
            return render(request, "depots/import_review.html", ctx)
        # Opening an applied receipt is local, even if its original Figma profile is offline.
        applied = ImportAnalysis.objects.select_related("result_revision__parent").filter(
            submission_id=submission_id, result_revision__site=site, state="applied"
        ).first()
        a = ctx["analysis"] = applied or imports.current(*args)
        if a and a.state == "review":
            review_context(ctx, request)
        elif a and a.state == "applied":
            ctx["imported_pages"] = result_pages(a)
        if post:
            if not a:
                raise ValidationError("Lancez d’abord l’analyse de cette remise.")
            token = params.get("token", "")
            if action == "select":
                imports.select_frames(*args, token, params.getlist("frame"))
                return redirect(request.path)
            if action == "destinations" and a.state == "review" and ctx["screen"] == "destinations":
                forms = ctx["frame_forms"]
                valid = [form.is_valid() for _, form in forms]
                if not all(valid):
                    ctx["input_error"] = True
                    raise ValidationError("Corrigez les destinations indiquées.")
                choices = [{"frame_id": frame["id"], **form.cleaned_data} for frame, form in forms]
                imports.save_review(*args, token, a.decisions, choices)
                return redirect(request.path)
            if action == "decision" and a.state == "review" and ctx["screen"] == "node":
                verdict = params.get("verdict")
                form = ctx["decision_form"]
                if verdict == "exclude":
                    choice = {"action": "exclude"}
                elif verdict == "accept" and ctx["candidate"] and form.is_valid():
                    choice = form.decision(verdict)
                else:
                    ctx["input_error"] = True
                    raise ValidationError("Choisissez une définition compatible et vérifiez les valeurs indiquées avant de conserver cette ligne.")
                imports.save_review(*args, token, {**a.decisions, ctx["node"]["id"]: choice}, a.destinations)
                return redirect(request.path + "?" + urlencode({"p": request.GET.get("p", "1")}) + "#correspondances")
            raise ValidationError("Cette action ne correspond pas à l’étape en cours.")
    except (ValidationError, registry.Conflict) as error:
        status = 422 if isinstance(error, ValidationError) else 409
        ctx["error"] = " ".join(error.messages) if isinstance(error, ValidationError) else str(error)
        # Do not redisplay cached design details after a provider or scope failure.
        if not ctx.get("input_error"):
            ctx["analysis"] = None
    return render(request, "depots/import_review.html", ctx, status=status)
