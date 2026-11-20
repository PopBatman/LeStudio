"""Comparaison privée d'une frame confirmée avec le rendu du brouillon."""

from hashlib import sha256
from urllib.parse import urlencode
from uuid import UUID, uuid4

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.debug import sensitive_post_parameters

from composition import preview_views as preview
from composition.builder_views import layers_for
from composition.models import CompositionRevision
from composition.preview import PreviewError
from registre import services as registry
from registre.views import require_manager, screen

from . import comparison, provenance
from .models import ComparisonDecision


FORMATS = {"desktop": ("Bureau", 1200), "tablet": ("Tablette", 820), "mobile": ("Mobile", 390)}
KINDS = {"correct": "À corriger", "accepted": "Écart accepté", "matched": "Aucun écart constaté"}


def query(path, **values):
    params = urlencode({k: v for k, v in values.items() if v is not None and v != ""})
    return path + ("?" + params if params else "")


def receipt_for(request, site_id, revision_id, page_id):
    value = request.GET.get("ticket")
    if not value:
        return None
    try:
        identity = UUID(value)
    except ValueError:
        raise Http404 from None
    receipt = preview.get_ticket(request, site_id, identity)
    if receipt.revision_id != revision_id or receipt.page_id != page_id:
        raise Http404
    return receipt


def select_frame(frames, params):
    identity, fmt = params.get("frame"), params.get("format")
    if fmt and fmt not in FORMATS:
        raise Http404
    if not frames:
        return None, fmt or "desktop"
    if identity:
        frame = next((f for f in frames if f["id"] == identity), None)
        if not frame or (fmt and frame["format"] != fmt):
            raise Http404
        return frame, frame["format"]
    if fmt:
        return next((f for f in frames if f["format"] == fmt), None), fmt
    frame = next((f for f in frames if f.get("base")), frames[0] if frames else None)
    return frame, frame["format"] if frame else "desktop"


def write_action(request, site, revision, page_id, source, frame, fmt, receipt):
    form = request.POST
    action = form.get("action")
    page_id = str(page_id)
    address = dict(frame=frame and frame["id"], format=fmt, target=request.GET.get("target"))
    if action == "prepare":
        started = timezone.now()
        result = preview.render_preview(request.user, site.pk, str(revision.pk), page_id)
        require_manager(request.user, site)
        receipt = preview.issue(request, revision.pk, page_id, started, result)
        if not receipt:
            raise registry.Conflict("La préparation a expiré. Relancez le rendu.")
    elif not frame or not source["detail_available"] or form.get("confirmed") != "1":
        raise ValidationError("Vérifiez la frame et confirmez votre choix.")
    elif action == "attach":
        comparison.attach_reference(
            request.user,
            site.pk,
            source["analysis_id"],
            page_id,
            frame["id"],
            form.get("version"),
            form.get("format"),
            request.FILES.get("image"),
            revision_id=revision.pk,
            previous=form.get("previous_reference", ""),
        )
    elif action == "decide":
        if not receipt or form.get("ticket") != str(receipt.pk):
            raise ValidationError("Préparez à nouveau le rendu de cette page.")
        if (form.get("target") or "") != (request.GET.get("target") or ""):
            raise ValidationError("Sélectionnez à nouveau l’élément à examiner.")
        comparison.save_decision(
            request,
            site.pk,
            source["analysis_id"],
            page_id,
            frame["id"],
            reference_id=form.get("reference"),
            ticket_id=receipt.pk,
            revision_id=revision.pk,
            format=fmt,
            width=form.get("width"),
            target=form.get("target") or "",
            kind=form.get("kind"),
            note=form.get("note", ""),
            previous=form.get("previous", ""),
            key=form.get("key"),
        )
    else:
        raise ValidationError("Action inconnue.")
    return redirect(query(request.path, **address, ticket=receipt and receipt.pk))


def comparison_screen(request, site, revision, page, source, frame, fmt, receipt, error, status):
    result, render_error = None, ""
    if receipt:
        result, render_error, code = preview.verified(request, receipt)
        if request.method == "HEAD" and result is None:
            return HttpResponse(status=code)
        require_manager(request.user, site)
        # The remote render can overlap erasure of the submission or loss of its mapping.
        source = provenance.for_page(request.user, site.pk, revision.pk, page["id"])
        if not source:
            raise Http404
        if frame:
            frame = next((f for f in source["frames"] if f["id"] == frame["id"]), None)
            if not frame:
                return redirect(request.path)
    head = (
        CompositionRevision.objects.filter(site=site).order_by("-number").values_list("pk", flat=True).first()
    )
    detail = source["detail_available"]
    reference = comparison.current_reference(source["analysis_id"], frame["id"]) if detail and frame else None
    address = dict(frame=frame and frame["id"], format=fmt, ticket=receipt and receipt.pk)
    target = request.GET.get("target") or ""
    target_labels = {"": "Page entière"}
    target_labels.update(
        {
            r["id"]: r["label"] + (" · " + r["summary"][:60] if r["summary"] else "")
            for r in layers_for(site, page)
        }
    )
    if target not in target_labels:
        raise Http404
    decisions = ComparisonDecision.objects.none()
    if detail:
        decisions = (
            ComparisonDecision.objects.filter(
                reference__analysis_id=source["analysis_id"], page_id=page["id"]
            )
            .select_related("reference", "author", "revision")
            .defer("reference__png", "revision__document")
            .order_by("-created_at", "-pk")
        )
    latest = None
    if frame:
        latest = decisions.filter(
            reference__frame_id=frame["id"], reference__format=fmt, target=target or None
        ).first()
    last_id = decisions.values_list("pk", flat=True).first()
    state_data = [
        detail,
        source.get("version"),
        source.get("submission_number"),
        head,
        reference and reference.pk,
        last_id,
        receipt and receipt.fingerprint,
        bool(result),
    ]
    access_state = sha256(str(state_data).encode()).hexdigest()
    if request.method == "HEAD":
        return HttpResponse(status=204, headers={"X-Compare-State": access_state})

    canvas = query(reverse("registre:site-builder", args=[site.pk]), revision=revision.pk, page=page["id"])

    def editor_url(occurrence=None):
        return query(
            reverse("registre:site-builder", args=[site.pk]),
            revision=revision.pk,
            page=page["id"],
            edit=1,
            selection=occurrence,
        )

    frames = source["frames"]
    frame_names = {f["id"]: f["name"] for f in frames}
    for item in frames:
        item.update(label=item["name"], url=query(request.path, frame=item["id"], ticket=address["ticket"]))
        for row in item["rows"]:
            if row.get("selectable"):
                if revision.pk == head:
                    row["edit_url"] = editor_url(row["occurrence"])
                elif receipt:
                    row["edit_url"] = query(
                        reverse("registre:builder-view", args=[site.pk, receipt.pk]),
                        selection=row["occurrence"],
                    )

    raw_width = frame and frame.get("width")
    width_attested = raw_width is not None and 1 <= raw_width <= comparison.MAX_DIMENSION
    width = raw_width if width_attested else FORMATS[fmt][1]

    def decision_row(d):
        current = bool(
            frame
            and reference
            and result
            and d.reference_id == reference.pk
            and d.revision_id == revision.pk
            and d.width == width
            and d.render_digest == receipt.fingerprint
            and revision.pk == head
        )
        return dict(
            id=d.pk,
            kind=d.kind,
            label=KINDS[d.kind],
            note=d.note,
            target=d.target,
            target_label=target_labels.get(str(d.target) if d.target else "", "Occurrence retirée"),
            author=d.author,
            created_at=d.created_at,
            number=d.revision.number,
            format=FORMATS.get(d.reference.format, (d.reference.format,))[0],
            frame_name=frame_names.get(d.reference.frame_id, d.reference.frame_id),
            current=current,
            width=d.width,
            reference_version=d.reference.version,
            reference_digest=d.reference.digest,
            reference_id=d.reference_id,
            render_digest=d.render_digest,
            instance_id=d.instance_id,
        )

    last = decision_row(latest) if latest else None
    current_state = "À examiner"
    if not (frame and reference and result and width_attested):
        current_state = "Comparaison indisponible"
    elif last:
        current_state = last["label"] if last["current"] else "À réexaminer"

    targets = [{"id": identity, "label": label} for identity, label in target_labels.items()]
    # Retain every decision while keeping the first screen bounded.
    history_page = Paginator(decisions, 30).get_page(request.GET.get("history"))
    ctx = dict(
        site=site,
        revision=revision,
        page=page,
        provenance=source,
        frame=frame,
        frames=frames,
        format=fmt,
        format_label=FORMATS[fmt][0],
        formats=[
            dict(
                id=k,
                label=v[0],
                selected=k == fmt,
                url=query(request.path, format=k, ticket=address["ticket"]),
            )
            for k, v in FORMATS.items()
        ],
        receipt=receipt,
        ticket=receipt and receipt.pk,
        document_url=reverse("registre:preview-document", args=[site.pk, receipt.pk]) if result else "",
        reference=reference,
        reference_url=reverse("registre:figma-reference", args=[site.pk, reference.pk]) if reference else "",
        width=width,
        width_attested=width_attested,
        error=error,
        render_error=render_error,
        draft_note=request.POST.get("note", "")[:1000] if error else "",
        draft_kind=request.POST.get("kind") if error else "",
        history=[decision_row(d) for d in history_page],
        history_next=query(request.path, **address, target=target, history=history_page.next_page_number())
        if history_page.has_next()
        else "",
        history_prev=query(
            request.path, **address, target=target, history=history_page.previous_page_number()
        )
        if history_page.has_previous()
        else "",
        canvas_url=canvas,
        edit_url=editor_url(target) if head == revision.pk else "",
        head_current=head == revision.pk,
        access_url=query(request.path, **address, target=target),
        access_state=access_state,
        target=target,
        targets=targets,
        previous=str(latest.pk) if latest else "",
        last_decision=last,
        decision_allowed=bool(frame and reference and result and revision.pk == head and width_attested),
        upload_allowed=bool(frame and detail and revision.pk == head),
        current_state=current_state,
        form_key=uuid4(),
        expires_ms=int(receipt.expires_at.timestamp() * 1000) if receipt else 0,
    )
    return render(request, "composition/figma_compare.html", ctx, status=status)


@screen("GET", "HEAD", "POST")
@sensitive_post_parameters()
def compare(request, pk, revision_id, page_id):
    site = get_object_or_404(registry.sites(request.user), pk=pk)
    require_manager(request.user, site)
    revision = get_object_or_404(CompositionRevision, site=site, pk=revision_id)
    page = preview.lookup_page(revision.document, str(page_id))
    source = provenance.for_page(request.user, pk, revision_id, str(page_id)) if page else None
    if not source:
        raise Http404
    frame, fmt = select_frame(source["frames"], request.GET)
    receipt = receipt_for(request, pk, revision_id, page_id)
    error, status = "", 200
    if request.method == "POST":
        try:
            return write_action(request, site, revision, page_id, source, frame, fmt, receipt)
        except (ValidationError, registry.Conflict, PreviewError) as exc:
            status = 422 if isinstance(exc, ValidationError) else 409
            error = " ".join(exc.messages) if isinstance(exc, ValidationError) else str(exc)
            if request.POST.get("action") == "prepare":
                receipt = None
    return comparison_screen(request, site, revision, page, source, frame, fmt, receipt, error, status)


@screen("GET", "HEAD")
def image(request, pk, reference_id):
    content = comparison.reference_png(request.user, pk, reference_id)
    return HttpResponse(
        content,
        content_type="image/png",
        headers={"X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer"},
    )
