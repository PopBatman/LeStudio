from django import forms

from .catalogue_forms import BlockForm, RemoveForm, ref
from .validation import _external_url


ACTIONS = {
    "article_reference": "Référence éditoriale Wagtail",
    "block_place": "Régler le placement", "parent_layout": "Disposition responsive",
    "section_add": "Ajouter une section", "section_edit": "Régler la section",
    "section_move": "Déplacer la section", "section_remove": "Retirer la section",
    "block_add": "Ajouter un bloc", "block_edit": "Modifier le bloc",
    "block_move": "Déplacer le bloc", "block_remove": "Retirer le bloc",
}


class ArticleForm(forms.Form):
    page_number = forms.IntegerField(label="Identifiant de la page Wagtail", min_value=1,
                                     max_value=2147483647)


class LayoutForm(forms.Form):
    display = forms.ChoiceField(label="Disposition", choices=[("stack", "Pile"), ("grid", "Grille")])
    columns = forms.IntegerField(label="Colonnes", min_value=1, max_value=12, required=False)
    gap = forms.IntegerField(label="Espacement (px)", min_value=0, max_value=128, required=False)

    def clean(self):
        values = super().clean()
        if values.get("display") == "stack" and (values.get("columns") or 1) > 1:
            self.add_error("columns", "Une pile occupe une seule colonne.")
        return values


def secure_url(value):
    try:
        _external_url(value, "destination")
    except forms.ValidationError as exc:
        raise forms.ValidationError("Saisissez une adresse HTTPS complète.") from exc


def editor_form(ctx, data):
    action, section, block = ctx["action"], ctx["section"], ctx["occurrence"]
    entity, verb = action.split("_")
    if entity == "block" and verb in ("add", "edit"):
        chosen = ctx["chosen"]
        if not chosen:
            return None
        initial = block if verb == "edit" else {"definition": ref(chosen), "props": {}}
        same = verb == "edit" and ctx["pinned"] and ctx["pinned"]["renderer"] == chosen["renderer"]
        form = BlockForm(chosen, ctx["medias"], initial, same, data)
        if "prop_url" in form.fields:
            form.fields["prop_url"].validators.append(secure_url)
    elif entity == "section" and verb in ("add", "edit"):
        layout = section["layout"]["base"] if verb == "edit" else {}
        form = LayoutForm(data=data, initial={"display": "stack", **layout})
    elif verb == "remove":
        return RemoveForm(data=data)
    else:
        form = forms.Form(data=data)
    if verb in ("add", "move"):
        rows = ctx["sections"]
        if entity == "block":
            parents, targets = [], []
            blocked = {block["id"]} if block and verb == "move" else set()
            for item in rows:
                parents.append((item["id"], item["label"]))
                labels = {item["id"]: item["label"]}
                for row in item["rows"]:
                    if row["id"] in blocked or row["parent_id"] in blocked:
                        blocked.add(row["id"])
                        continue
                    label = f'{labels[row["parent_id"]]} / {row["label"]} {row["index"]}'
                    labels[row["id"]] = label
                    targets.append((row["id"], label))
                    if row["is_container"]:
                        parents.append((row["id"], label))
            default = block["parent_id"] if block else section["id"]
            if block and verb == "add" and block["is_container"]:
                default = block["id"]
            form.fields["parent"] = forms.ChoiceField(label="Destination", choices=parents)
            form.initial["parent"] = default
        else:
            targets = [(s["id"], s["label"]) for s in rows if verb == "add" or s != section]
        form.fields["before"] = forms.ChoiceField(label="Insérer avant", required=False,
                choices=[("", "À la fin de la destination"), *targets])
        if verb == "move":
            selected = block if entity == "block" else section
            form.initial["before"] = selected["next_id"]
    return form


def command(ctx):
    action, form = ctx["action"], ctx["form"]
    entity, verb = action.split("_")
    values = form.cleaned_data
    result = {"action": action, "page": ctx["page_id"]}
    if verb != "add":
        result["id"] = ctx["node_id"] if entity == "block" else ctx["section_id"]
    if verb in ("add", "move"):
        result["before"] = values["before"] or None
        if entity == "block":
            result["parent"] = values["parent"]
    if verb in ("add", "edit"):
        if entity == "block":
            chosen = ctx["chosen"]
            result.update(definition=ref(chosen), props=form.parameters(chosen["props"]), appearance=form.appearance())
        else:
            base = {k: values[k] for k in ("display", "columns", "gap") if values.get(k) is not None}
            original = ctx["section"]["layout"] if verb == "edit" else {}
            # Preserve the implicit display of historical sections during a no-op.
            if verb == "edit" and "display" not in original["base"] and base["display"] == "stack":
                del base["display"]
            result["layout"] = {**original, "base": base}
    if verb == "remove":
        result["confirmed"] = values["confirmed"]
    return result
