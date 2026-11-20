"""Read confirmed local import receipts in the context of an immutable Studio page."""
from django.core.exceptions import PermissionDenied
from django.db import connection
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from composition.models import CompositionRevision
from registre import services as registry
from .models import ImportAnalysis
from .services import RETENTION

FORMATS = ("desktop", "tablet", "mobile")


def result_pages(analysis):
    """Imported pages are precisely the new UUIDs in this creation/append revision.

    This also works on the deliberately minimized receipt returned by a replay.
    """
    result = analysis.result_revision
    previous = {p["id"] for p in result.parent.document["pages"]} if result.parent_id else set()
    return [p for p in result.document["pages"] if p["id"] not in previous]


def _import_id(site_id, revision, page_id):
    receipts = ImportAnalysis.objects.filter(
        state="applied", result_revision__site_id=site_id, result_revision__number__lte=revision.number
    )
    if connection.features.supports_json_field_contains:
        contains_page = [{"id": page_id}]
        receipts = receipts.filter(result_revision__document__pages__contains=contains_page).exclude(
            result_revision__parent__document__pages__contains=contains_page
        )
        matches = list(receipts.values_list("pk", "result_revision_id"))
    else:
        receipts = receipts.select_related("result_revision__parent").only(
            "pk", "result_revision__id", "result_revision__document",
            "result_revision__parent__id", "result_revision__parent__document",
        )
        matches = [(r.pk, r.result_revision_id) for r in receipts
                   if any(p["id"] == page_id for p in result_pages(r))]
    if not matches:
        return None
    # Follow actual parent identities, including when examining an older revision.
    by_revision = {rev: analysis for analysis, rev in matches}
    if revision.pk in by_revision:
        return by_revision[revision.pk]
    parents = dict(CompositionRevision.objects.filter(site_id=site_id, number__lt=revision.number)
                   .values_list("pk", "parent_id"))
    ancestor = revision.parent_id
    while ancestor is not None:
        if ancestor in by_revision:
            return by_revision[ancestor]
        ancestor = parents.pop(ancestor, None)
    return None


def is_imported_page(site_id, revision_id, page_id):
    """For the authorized canvas shell, whose current page is already validated."""
    revision = CompositionRevision.objects.filter(site_id=site_id, pk=revision_id).only("number","parent_id").first()
    return bool(revision and _import_id(site_id, revision, str(page_id)))


def _dimension(value):
    if type(value) in (int, float) and 0 < value <= 10_000_000:
        return max(1, round(value))
    return None


def frame_metadata(analysis, page_id):
    """Return only frames attested for this exact page and still-live submission."""
    source = analysis.submission
    if (analysis.state != "applied" or not source or source.erased_at
            or source.created_at <= timezone.now() - RETENTION or not analysis.version
            or source.invitation.site_id != analysis.result_revision.site_id):
        return []
    frames = {f["id"]: f for f in analysis.observation.get("frames", [])}
    records = []
    for d in analysis.destinations:
        frame_id = d.get("frame_id")
        if (analysis.mapping.get(frame_id) != str(page_id)
                or frame_id not in frames or d.get("format") not in FORMATS):
            continue
        f = frames[frame_id]
        records.append({"id":frame_id, "name":f.get("name") or frame_id,
                        "format":d["format"], "base":d.get("base", False),
                        "width":_dimension(f.get("width")), "height":_dimension(f.get("height"))})
    return records


def _blocks(page):
    def descendants(block, section_id):
        yield block["id"], (section_id, block)
        for child in block.get("children", []):
            yield from descendants(child, section_id)
    return dict(item for section in page["sections"] for block in section["blocks"]
                for item in descendants(block, section["id"]))


def _row(analysis, proposal, frame, original, current):
    key = proposal["id"]
    occurrence = analysis.mapping.get(key + "@container" if key == frame["id"] else key)
    imported = original.get(occurrence)
    decision = analysis.decisions.get(key, {})
    action = decision.get("action", "")
    task = None
    if action == "exclude" and not proposal.get("candidates"):
        # A confirmed exclusion is the durable work item. Reopening it has no side effects.
        task = {"id": f"{analysis.pk}/{key}", "label":proposal["name"], "status":"À instruire"}
    block = imported[1] if imported else {}
    appearance = block.get("appearance", {})
    retained = dict(appearance.get("tokens", {}))
    token_names = sorted(set(proposal.get("tokens", {})) | set(decision.get("tokens", {})) | set(retained))
    token_rows = []
    layout = block.get("props", {}).get("layout")
    for name in token_names:
        observed = proposal.get("tokens", {}).get(name)
        value = retained.get(name)
        if name == "gap" and isinstance(layout, dict):
            effective = {**layout.get("base", {}), **layout.get(frame["format"], {})}
            value = effective.get("gap")
        token_rows.append({"name":name, "observed":observed, "value":value})
    return {"name":proposal["name"], "node_id":key, "occurrence":occurrence,
            "selectable":occurrence in current, "definition":block.get("definition"),
            "section_id":imported[0] if imported else None, "variant":appearance.get("variant", ""),
            "tokens":retained, "token_rows":token_rows, "gaps":proposal.get("gaps", []),
            "reason":proposal.get("reason", ""), "decision":action, "task":task}


def for_page(actor, site_id, revision_id, page_id):
    site = get_object_or_404(registry.sites(actor), pk=site_id)
    if not registry.can_manage(actor, site):
        raise PermissionDenied
    revision = get_object_or_404(CompositionRevision, pk=revision_id, site_id=site.pk)
    page_id = str(page_id)
    page = next((p for p in revision.document["pages"] if p["id"] == page_id), None)
    if page is None:
        raise Http404
    identity = _import_id(site.pk, revision, page_id)
    if identity is None:
        return None
    analysis = get_object_or_404(ImportAnalysis.objects.select_related(
        "submission__invitation", "result_revision__author"), pk=identity, result_revision__site=site)
    imported = analysis.result_revision
    source_page = next(p for p in imported.document["pages"] if p["id"] == page_id)
    frames = frame_metadata(analysis, page_id)
    context = {
        "analysis_id":str(analysis.pk), "import_number":imported.number, "import_revision":str(imported.pk),
        "submission_number":None, "version":"", "author":imported.author.get_username() if imported.author else "",
        "detail_available":bool(frames), "frames":frames, "local_blocks":[], "missing_formats":[],
    }
    if not frames:
        return context
    original, current = _blocks(source_page), _blocks(page)
    represented = set()
    for frame in frames:
        root = original.get(analysis.mapping.get(frame["id"] + "@container"))
        frame["section_id"] = root[0] if root else None
        frame["rows"] = [_row(analysis, p, frame, original, current) for p in analysis.proposals
                         if p.get("frame_id") == frame["id"]]
        represented.update(r["occurrence"] for r in frame["rows"])
    formats = {f["format"] for f in frames}
    context.update(submission_number=analysis.submission.version, version=analysis.version,
                   missing_formats=[f for f in FORMATS if f not in formats],
                   local_blocks=[{"id":key, "label":block["definition"]["key"]} for key, (_,block) in current.items()
                                 if key not in represented])
    return context
