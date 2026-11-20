from django import forms

ACTIONS = {
    "page_add": "Créer une page", "page_edit": "Modifier la page",
    "page_move": "Déplacer la page", "page_delete": "Supprimer la branche",
    "menu_add": "Créer un menu", "menu_edit": "Renommer le menu", "menu_delete": "Supprimer le menu",
    "item_add": "Ajouter une entrée", "item_edit": "Modifier l’entrée",
    "item_move": "Déplacer l’entrée", "item_delete": "Retirer l’entrée",
}
FORMATS = [("desktop", "Bureau"), ("tablet", "Tablette"), ("mobile", "Mobile")]


def tree_rows(nodes):
    children = {}
    for node in nodes:
        children.setdefault(node["parent_id"], []).append(node)

    def visit(parent, depth):
        for node in children.get(parent, ()):
            yield {**node, "depth": depth}
            yield from visit(node["id"], depth + 1)
    return list(visit(None, 0))


def choices(nodes, field):
    return [(n["id"], "— " * n["depth"] + n[field]) for n in nodes]


class EditForm(forms.Form):
    def __init__(self, action, node, page_rows, item_rows, data=None):
        super().__init__(data=data)
        entity, operation = action.split("_")
        node = node or {}
        self.initial.update(node)
        if operation == "delete":
            if entity == "item" and any(row["parent_id"] == node.get("id") for row in item_rows):
                self.fields["branch"] = forms.BooleanField(label="Retirer aussi toutes les sous-entrées")
            return
        if operation in {"edit", "add"}:
            name = "title" if entity == "page" else "label"
            self.fields[name] = forms.CharField(label="Titre" if entity == "page" else "Libellé", max_length=120)
            if entity == "page" and (operation == "add" or node.get("parent_id") is not None):
                self.fields["slug"] = forms.RegexField(label="Segment d’URL", max_length=80,
                    regex=r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z",
                    help_text="Lettres minuscules, chiffres et tirets. Exemple : carnet-de-saison.")
            if entity == "item":
                target = node.get("target", {})
                self.initial.update(kind=target.get("kind", "page"), page_id=target.get("page_id"),
                                    url=target.get("url"), visibility=node.get("visibility", [key for key, _ in FORMATS]))
                self.fields["kind"] = forms.ChoiceField(label="Type d’entrée", choices=[
                    ("page", "Page du brouillon"), ("external", "Lien externe"), ("group", "Groupe sans lien")])
                self.fields["page_id"] = forms.ChoiceField(label="Page cible pour un lien interne", required=False,
                                                          choices=[("", "Choisir une page"), *choices(page_rows, "title")])
                self.fields["url"] = forms.CharField(label="Adresse HTTPS pour un lien externe", required=False, max_length=2048)
                self.fields["visibility"] = forms.MultipleChoiceField(label="Formats de cette entrée (limités par ses parents)", choices=FORMATS,
                                                                      widget=forms.CheckboxSelectMultiple)
        if operation in {"add", "move"} and entity != "menu":
            nodes = page_rows if entity == "page" else item_rows
            eligible = []
            blocked = set()
            if node:
                blocked.add(node["id"])
            for row in nodes:
                if row["id"] in blocked or row["parent_id"] in blocked:
                    blocked.add(row["id"])
                else:
                    eligible.append(row)
            options = choices(eligible, "title" if entity == "page" else "label")
            parents = options if entity == "page" else [("", "Premier niveau"), *options]
            self.fields["parent_id"] = forms.ChoiceField(label="Parent", required=entity == "page", choices=parents)
            self.fields["before_id"] = forms.ChoiceField(
                label="Position", required=False, choices=[("", "En fin de liste"), *options],
                help_text="Pour insérer avant un élément, choisissez un frère du même parent.")

    def clean(self):
        data = super().clean()
        kind = data.get("kind")
        if kind == "page" and not data.get("page_id"):
            self.add_error("page_id", "Choisissez une page de ce brouillon.")
        elif kind == "external" and not data.get("url"):
            self.add_error("url", "Saisissez une adresse HTTPS.")
        return data

    def command(self, action, identity, menu_id):
        data = dict(self.cleaned_data)
        kind = data.pop("kind", None)
        if kind:
            page, url = data.pop("page_id"), data.pop("url")
            data["target"] = {"kind": kind}
            if kind == "page":
                data["target"]["page_id"] = page
            elif kind == "external":
                data["target"]["url"] = url
        for name in ("parent_id", "before_id"):
            if name in data:
                data[name] = data[name] or None
        if action == "page_edit":
            data.setdefault("slug", "")
        if identity:
            data["id"] = identity
        if action.startswith("item_"):
            data["menu_id"] = menu_id
        return {"action": action, **data}
