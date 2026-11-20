from django.urls import reverse

from .catalogue_views import sample_values
from .placement import effective_layout, effective_placement


def surface(ctx):
    fmt = ctx["format"]
    media = {m["id"]:reverse("registre:site-media", args=[ctx["site"].pk, m["id"]]) for m in ctx["medias"]}
    theme = ctx["head"]["document"]["theme"]
    result = []
    for section in ctx["sections"]:
        root = {"id":section["id"], "label":section["label"], "layout":effective_layout(section["layout"], fmt),
                "items":[], "min_height":0}
        parents = {root["id"]:root}
        for row in section["rows"]:
            pinned = row["pinned"]
            renderer = pinned["renderer"] if pinned else "unknown"
            if renderer == "container" and not row["is_container"]:
                renderer = "unknown"
            props = row["props"]
            media_ref = props.get("media")
            preview = sample_values(theme, pinned, row)
            font = "system-ui" if preview["system_font"] else "'DM Sans', sans-serif"
            style = (f"--cv-accent:{preview['accent']};--cv-ink:{preview['ink']};"
                     f"--cv-background:{preview['background']};--cv-gap:{preview['gap']}px;font-family:{font}")
            placement = effective_placement(row.get("placement", {}), fmt)
            layout = props.get("layout", {}) if renderer == "container" else {}
            node = {**row, "renderer":renderer, "appearance_style":style, "variant":preview["variant"],
                    "placement":placement, "layout":effective_layout(layout, fmt), "items":[], "min_height":0,
                    "media_url":media.get(media_ref.get("ref_id")) if isinstance(media_ref, dict) else ""}
            parent = parents[row["parent_id"]]
            parent["items"].append(node)
            if placement["mode"] == "free":
                parent["min_height"] = max(parent["min_height"], placement["y"] + placement["height"])
            parents[node["id"]] = node
        result.append(root)
    return result
