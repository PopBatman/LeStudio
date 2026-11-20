from django import forms

COLORS = {"accent": "Couleur d’accent", "background": "Couleur de fond", "ink": "Couleur du texte"}
FONTS = [("", "Hériter"), ("dm-sans", "DM Sans"), ("system", "Police du système")]
VARIANTS = {"default": "Standard", "primary": "Pleine", "secondary": "Contour"}
PARAMETERS = {"text": "Texte", "level": "Niveau du titre", "url": "Destination HTTPS",
              "label": "Libellé", "alt": "Texte alternatif", "media": "Image"}
THEME_KEYS = (*COLORS, "font", "gap", "media")


def token_fields(keys, medias):
    fields = {}
    for key in keys:
        if key in COLORS:
            fields[key] = forms.RegexField(label=COLORS[key], regex=r"\A#[0-9A-Fa-f]{6}\Z", max_length=7,
                                           required=False, widget=forms.TextInput(attrs={"placeholder": "#245A49"}))
        elif key == "font":
            fields[key] = forms.ChoiceField(label="Typographie", choices=FONTS, required=False)
        elif key == "gap":
            fields[key] = forms.IntegerField(label="Espacement (px)", min_value=0, max_value=128, required=False)
        elif key == "media":
            fields[key] = forms.ChoiceField(label="Média du site", required=False, choices=[
                ("", "Aucun"), *((m["id"], m["label"]) for m in medias)])
    return fields


def token_values(fields, data):
    values = {key: data[key] for key in fields if data.get(key) not in (None, "")}
    if "media" in values:
        values["media"] = {"kind": "media", "ref_id": values["media"]}
    return values


class AppearanceForm(forms.Form):
    def __init__(self, action, definition, medias, initial, data=None):
        super().__init__(data=data, initial=dict(initial))
        keys = THEME_KEYS if action == "theme" else definition["tokens"]
        if action != "theme":
            self.fields["variant"] = forms.ChoiceField(label="Variante", required=False, choices=[
                ("", "Hériter"), *((v, VARIANTS.get(v, v)) for v in definition["variants"])])
        self.fields.update(token_fields(keys, medias))
        self.keys = keys
        if isinstance(self.initial.get("media"), dict):
            self.initial["media"] = self.initial["media"].get("ref_id")

    def appearance(self):
        result = {}
        if self.cleaned_data["variant"]:
            result["variant"] = self.cleaned_data["variant"]
        tokens = token_values(self.keys, self.cleaned_data)
        if tokens:
            result["tokens"] = tokens
        return result


class BlockForm(AppearanceForm):
    def __init__(self, definition, medias, block, same_renderer, data=None):
        style = block.get("appearance", {}) if block["definition"] == ref(definition) else {}
        super().__init__("block", definition, medias, {**style.get("tokens", {}), "variant": style.get("variant")}, data)
        self.props = {}
        options = [(m["id"], m["label"]) for m in medias]
        for name, kind in definition["props"].items():
            label = PARAMETERS.get(name, name)
            key = "prop_" + name
            value = block["props"].get(name) if same_renderer else None
            if kind == "layout":
                self.props[name] = value or {"base": {"display": "stack"}}
                continue
            if kind == "media":
                field = forms.ChoiceField(label=label, choices=[("", "Choisir une image"), *options])
                value = value.get("ref_id") if isinstance(value, dict) else None
            elif kind == "level":
                field = forms.TypedChoiceField(label=label, choices=[(i, str(i)) for i in range(1, 7)], coerce=int)
            elif kind == "https":
                field = forms.CharField(label=label, max_length=2048)
            else:
                field = forms.CharField(label=label, max_length={"label": 120, "alt": 300}.get(kind, 4000))
            self.fields[key] = field
            self.initial[key] = value

    def parameters(self, schema):
        props = dict(self.props)
        for key, kind in schema.items():
            if kind != "layout":
                value = self.cleaned_data["prop_" + key]
                props[key] = {"kind": "media", "ref_id": value} if kind == "media" else value
        return props


def ref(d):
    return {k: d[k] for k in ("scope", "key", "version")}


class PromotionForm(forms.Form):
    key = forms.SlugField(label="Clé globale", max_length=120)
    label = forms.CharField(label="Libellé public", max_length=120)
    rights = forms.CharField(label="Référence du justificatif des droits de réutilisation", max_length=250)
    reason = forms.CharField(label="Motif de la proposition", max_length=500, widget=forms.Textarea(attrs={"rows": 2}))


class ReviewForm(forms.Form):
    decision = forms.ChoiceField(label="Décision", choices=[("", "Choisir"), ("approve", "Accepter"), ("reject", "Refuser")])
    rights_checked = forms.BooleanField(label="Justificatif et droits de réutilisation vérifiés", required=False)
    technical_checked = forms.BooleanField(label="Rendu et copie expurgée examinés", required=False)
    note = forms.CharField(label="Motif de la décision", max_length=500, widget=forms.Textarea(attrs={"rows": 2}))


class RemoveForm(forms.Form):
    confirmed = forms.BooleanField(label="Confirmer le retrait de cette occurrence et de ses descendants")
