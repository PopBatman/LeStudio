from django.core.exceptions import ValidationError

from .appearance_contract import definition_key
from .validation import _layout


def indexed(rows):
    for index, row in enumerate(rows, 1):
        yield {**row, "index": index, "next_id": rows[index]["id"] if index < len(rows) else ""}


def block_rows(blocks, manifests, parent, depth=0):
    for row in indexed(blocks):
        pinned = manifests.get(definition_key(row["definition"]))
        props = row["props"]
        is_container = bool(pinned and pinned["renderer"] == "container")
        if is_container:
            # Historical definitions can pin a textual property also named layout.
            try:
                _layout(props.get("layout"), "layout")
            except ValidationError:
                is_container = False
        yield {**row, "parent_id": parent, "depth": depth, "pinned": pinned,
               "label": pinned["label"] if pinned else row["definition"]["key"],
               "summary": props.get("text") or props.get("label") or props.get("alt") or "",
               "is_container": is_container}
        yield from block_rows(row["children"], manifests, row["id"], depth + 1)
