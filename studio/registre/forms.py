from django import forms

from .models import Client


class VersionForm(forms.Form):
    version = forms.CharField(widget=forms.HiddenInput, required=False)


class ClientForm(VersionForm):
    client_type = forms.ChoiceField(label="Type de client", choices=Client.TYPES)
    display_name = forms.CharField(label="Nom du client", max_length=160)


class ContactForm(VersionForm):
    display_name = forms.CharField(label="Nom du contact", max_length=160)
    role = forms.CharField(label="Rôle principal", max_length=100)
    email = forms.EmailField(label="Courriel", max_length=254, required=False)
    phone = forms.CharField(label="Téléphone", max_length=32, required=False,
                            widget=forms.TextInput(attrs={"type": "tel"}),
                            help_text="Renseignez au moins un courriel ou un téléphone.")

    def clean(self):
        data = super().clean()
        if not self.errors and not (data.get("email") or data.get("phone")):
            message = "Renseignez au moins une coordonnée pour ce contact."
            self.add_error("email", message)
            self.add_error("phone", message)
        return data


class SiteForm(VersionForm):
    name = forms.CharField(label="Nom du site", max_length=160)
    site_type = forms.CharField(label="Type de site", required=False, max_length=80)
    domain = forms.CharField(label="Nom de domaine", max_length=254, required=False,
                             help_text="Facultatif. Vous pourrez le renseigner plus tard.")
    description = forms.CharField(label="Description", max_length=1000, required=False,
                                  widget=forms.Textarea(attrs={"rows": 3}))
