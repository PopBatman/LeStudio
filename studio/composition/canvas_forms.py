from django import forms

from .placement import BOUNDS, effective_layout, effective_placement


LABELS = {
    "mode": "Placement", "x": "Position X (%)", "y": "Position Y (px)",
    "width": "Largeur (%)", "height": "Hauteur (px)", "z": "Niveau de superposition",
    "span": "Colonnes occupées", "display": "Disposition", "columns": "Colonnes de la grille",
    "gap": "Espacement (px)",
}
LIMITS = {**BOUNDS, "columns": (1, 12), "gap": (0, 128)}
ENUMS = {"mode": [("flow", "Dans le flux"), ("free", "Libre")],
         "display": [("stack", "Pile"), ("grid", "Grille")]}
PLACEMENT_KEYS = ("mode", "x", "y", "width", "height", "z", "span")
LAYOUT_KEYS = ("display", "columns", "gap")


def settings(ctx, action):
    node, fmt = ctx["occurrence"], ctx["format"]
    if action == "block_place":
        stored = node.get("placement", {})
        effective = effective_placement(stored, fmt)
        keys = PLACEMENT_KEYS
    else:
        stored = node["props"].get("layout", {}) if node else ctx["section"]["layout"]
        effective = effective_layout(stored, fmt)
        keys = LAYOUT_KEYS
    return keys, effective, stored.get(fmt, {})


def setting_labels(keys, effective, local, fmt):
    rows = []
    for key in keys:
        if key not in effective:
            continue
        value = dict(ENUMS.get(key, ())).get(effective[key], effective[key])
        source = "réglé ici" if key in local else "hérité de la base" if fmt != "base" else "par défaut"
        rows.append((LABELS[key], f"{value} · {source}"))
    return rows


class CanvasForm(forms.Form):
    def __init__(self, ctx, data=None):
        super().__init__(data)
        keys, effective, local = settings(ctx, ctx["action"])
        for key in keys:
            if key in ENUMS:
                field = forms.ChoiceField(choices=[("", "Conserver"), *ENUMS[key]])
            else:
                low, high = LIMITS[key]
                field = forms.IntegerField(min_value=low, max_value=high,
                    widget=forms.NumberInput(attrs={"placeholder": effective.get(key, "—")}))
            field.label, field.required = LABELS[key], False
            self.fields[key] = field
        self.fields["clear"] = forms.MultipleChoiceField(label="Rétablir les valeurs héritées ou par défaut",
            choices=[(key, LABELS[key]) for key in keys if key in local or data and key in data.getlist("clear")],
            widget=forms.CheckboxSelectMultiple, required=False)
        for key in ("parent", "before"):
            if data and key in data and ctx["action"] == "block_place":
                self.fields[key] = forms.UUIDField(widget=forms.HiddenInput, required=key=="parent")
        self.keys = keys

    def add_domain_error(self, exc, ctx):
        details = getattr(exc, "params", None) or {}
        field = details.get("field")
        if details.get("block") != ctx["node_id"] or details.get("format") != ctx["format"] or field not in self.fields:
            field = None
        self.add_error(field, exc)

    def clean(self):
        values = super().clean()
        for key in values.get("clear", []):
            if values.get(key) not in ("", None):
                self.add_error(key, "Choisissez entre une nouvelle valeur et le retour à l’héritage.")
        return values

    def command(self, ctx):
        values = self.cleaned_data
        result = {"action":ctx["action"], "page":ctx["page_id"], "id":ctx["node_id"] or ctx["section_id"],
                  "format":ctx["format"], "patch":{k:values[k] for k in self.keys if values.get(k) not in ("", None)},
                  "clear":values["clear"]}
        if "parent" in values:
            result.update(parent=str(values["parent"]), before=str(values["before"]) if values.get("before") else None)
        return result
