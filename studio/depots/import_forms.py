"""Formulaires de revue d’une frame et d’une correspondance à la fois."""
import re

from django import forms
from django.utils.text import slugify

FORMATS = (("desktop", "Bureau"), ("tablet", "Tablette"), ("mobile", "Mobile"))
TOKEN_LABELS = {"ink": "Couleur du texte", "background": "Fond", "accent": "Accent",
                "font": "Police", "gap": "Espacement (px)"}


class DestinationForm(forms.Form):
    title = forms.CharField(label="Titre de la page", max_length=120)
    slug = forms.RegexField(label="Segment d’adresse", regex=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=80, required=False,
                           help_text="Laisser vide pour la page d’accueil du premier brouillon.")
    group = forms.CharField(label="Groupe de page", max_length=80,
                            help_text="Donnez le même groupe aux formats d’une même page.")
    format = forms.ChoiceField(label="Format observé", choices=(("", "Choisir le format"), *FORMATS))
    base = forms.BooleanField(label="Utiliser cette frame comme base du groupe", required=False)
    home = forms.BooleanField(label="Utiliser comme accueil du site", required=False)
    parent_id = forms.ChoiceField(label="Page parente", required=False)

    def __init__(self, frame, saved, pages, index, **kwargs):
        defaults = dict(group=frame["id"], title=frame["name"][:120], slug=re.sub(r"[-_]+", "-", slugify(frame["name"]))[:80].strip("-"),
                        format="", base=True)
        if not pages and index == 0:
            defaults.update(home=True, slug="")
        super().__init__(initial={**defaults, **saved}, prefix=f"f{index}", **kwargs)
        if pages:
            self.fields["parent_id"].choices = [(p["id"], p["title"]) for p in pages]
            self.fields["parent_id"].required = True
            del self.fields["home"]
        else:
            del self.fields["parent_id"]


class DecisionForm(forms.Form):
    def __init__(self, proposal, candidate, previous, media, **kwargs):
        super().__init__(**kwargs)
        self.component_renderer = candidate.get("renderer") if candidate else None
        self.definition = candidate.get("id") if candidate else None
        self.proposal = proposal
        props = {**proposal.get("props", {}), **previous.get("props", {})}
        renderer = self.component_renderer
        if renderer in ("text", "heading", "signature"):
            self.fields["text"] = forms.CharField(label="Texte du bloc", max_length=4000,
                widget=forms.Textarea(attrs={"rows": 2}), initial=props.get("text") or proposal.get("text"))
        if renderer == "heading":
            self.fields["level"] = forms.TypedChoiceField(label="Niveau du titre", coerce=int,
                choices=[(n, f"Titre {n}") for n in range(1, 7)], initial=props.get("level", 2))
        if renderer == "button":
            self.fields["label"] = forms.CharField(label="Libellé du bouton", max_length=120,
                initial=props.get("label") or proposal.get("text") or proposal["name"])
            self.fields["url"] = forms.URLField(label="Destination HTTPS", assume_scheme="https",
                initial=props.get("url"))
            self.fields["variant"] = forms.ChoiceField(label="Variante du bouton",
                choices=(("primary", "Principale"), ("secondary", "Secondaire")),
                initial=previous.get("variant") or proposal.get("variant") or "primary")
        if renderer == "image":
            self.fields["media"] = forms.ChoiceField(label="Média autorisé du site",
                choices=[("", "Choisir un média")] + [(m["id"], m["label"]) for m in media],
                initial=props.get("media", {}).get("ref_id"))
            self.fields["alt"] = forms.CharField(label="Alternative textuelle", max_length=250, initial=props.get("alt"))
        for key, observed in proposal.get("tokens", {}).items():
            if key not in TOKEN_LABELS:
                continue
            retained = previous.get("tokens", {})
            choice = None
            if previous:
                choice = "omit" if key not in retained else ("use" if retained[key] == observed else "edit")
            self.fields[f"pick_{key}"] = forms.ChoiceField(
                label=f"{TOKEN_LABELS[key]} · valeur observée {observed}",
                choices=(("", "Choisir"), ("use", "Accepter la valeur"), ("edit", "Corriger"), ("omit", "Écarter")),
                initial=choice)
            options = dict(label=f"{TOKEN_LABELS[key]} corrigé(e)", required=False, initial=retained.get(key, observed))
            if key == "gap":
                self.fields[key] = forms.IntegerField(min_value=0, max_value=128, **options)
            elif key == "font":
                self.fields[key] = forms.ChoiceField(choices=(("system", "Système"), ("dm-sans", "DM Sans")), **options)
            else:
                self.fields[key] = forms.RegexField(regex=r"^#[0-9a-fA-F]{6}$", max_length=7, **options)

    def clean(self):
        values = super().clean()
        for key in self.proposal.get("tokens", {}):
            if values.get(f"pick_{key}") == "edit" and values.get(key) in ("", None):
                self.add_error(key, "Indiquez la valeur corrigée.")
        if self.component_renderer == "button" and values.get("url") and not values["url"].startswith("https://"):
            self.add_error("url", "Indiquez une destination HTTPS.")
        return values

    def decision(self, action):
        values = self.cleaned_data
        props = {key: values[key] for key in ("text", "level", "label", "url", "alt") if key in values}
        if self.component_renderer == "image":
            props["media"] = {"kind": "media", "ref_id": values["media"]}
        if self.component_renderer == "container":
            props["layout"] = self.proposal.get("props", {}).get("layout", {"base": {}})
        tokens = {}
        for key, observed in self.proposal.get("tokens", {}).items():
            if values.get(f"pick_{key}") == "use":
                tokens[key] = observed
            elif values.get(f"pick_{key}") == "edit":
                tokens[key] = values[key]
        corrected = self.definition != self.proposal.get("suggested") or props != self.proposal.get("props", {})
        choice = {"action": "correct" if corrected else action, "definition": self.definition,
                  "props": props, "tokens": tokens}
        if self.component_renderer == "button":
            choice["variant"] = values["variant"]
        return choice
