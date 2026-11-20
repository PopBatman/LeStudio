import re
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Client(Record):
    TYPES = [
        ("COMPANY", "Entreprise"),
        ("ASSOCIATION", "Association"),
        ("INDIVIDUAL", "Particulier"),
    ]
    client_type = models.CharField("type de client", max_length=12, choices=TYPES)
    display_name = models.CharField("nom", max_length=160)
    archived_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["display_name", "id"]
        permissions = [("create_client", "Créer une fiche client dans Studio")]
        constraints = [
            models.CheckConstraint(
                condition=Q(client_type__in=["COMPANY", "ASSOCIATION", "INDIVIDUAL"]),
                name="registre_client_type",
            ),
            models.CheckConstraint(
                condition=Q(display_name__regex=r"\S"), name="registre_client_name"
            ),
        ]


class Site(Record):
    client = models.ForeignKey(Client, related_name="sites", on_delete=models.PROTECT)
    name = models.CharField("nom", max_length=160)
    site_type = models.CharField("type de site", max_length=80, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    domain = models.CharField("nom de domaine", max_length=253, blank=True)

    class Meta:
        ordering = ["name", "id"]
        constraints = [
            models.CheckConstraint(condition=Q(name__regex=r"\S"), name="registre_site_name")
        ]

    def clean(self):
        if not self.domain:
            return
        try:
            domain = self.domain.removesuffix(".").encode("idna").decode("ascii").lower()
        except UnicodeError:
            domain = ""
        label = r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
        if len(domain) > 253 or not all(re.fullmatch(label, item) for item in domain.split(".")):
            raise ValidationError(
                {"domain": "Saisissez un nom de domaine valide, sans protocole ni chemin."}
            )
        self.domain = domain


class Contact(Record):
    client = models.ForeignKey(Client, related_name="contacts", on_delete=models.PROTECT)
    display_name = models.CharField("nom", max_length=160)
    role = models.CharField("rôle principal", max_length=100)
    email = models.EmailField("courriel", blank=True)
    phone = models.CharField("téléphone", max_length=32, blank=True)

    class Meta:
        ordering = ["display_name", "id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(display_name__regex=r"\S") & Q(role__regex=r"\S"),
                name="registre_contact_labels",
            ),
            models.CheckConstraint(
                condition=Q(email__regex=r"\S") | Q(phone__regex=r"\S"),
                name="registre_contact_channel",
            ),
        ]

    def clean(self):
        if not self.email and not self.phone:
            raise ValidationError("Renseignez au moins un courriel ou un téléphone.")
        if self.email and "@" in self.email:
            local, domain = self.email.rsplit("@", 1)
            self.email = f"{local}@{domain.lower()}"
        if self.phone:
            digits = re.sub(r"[ ().-]", "", self.phone)
            if not re.fullmatch(r"\+?[0-9]{6,15}", digits):
                raise ValidationError(
                    {"phone": "Saisissez un numéro de téléphone de 6 à 15 chiffres."}
                )
            self.phone = digits


class Grant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    level = models.CharField(max_length=6, choices=[("read", "Lecture"), ("manage", "Gestion")])

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                condition=Q(level__in=["read", "manage"]), name="%(app_label)s_%(class)s_level"
            )
        ]


class ClientGrant(Grant):
    client = models.ForeignKey(Client, related_name="grants", on_delete=models.CASCADE)

    class Meta(Grant.Meta):
        constraints = Grant.Meta.constraints + [
            models.UniqueConstraint(fields=["user", "client"], name="registre_client_grant")
        ]


class SiteGrant(Grant):
    site = models.ForeignKey(Site, related_name="grants", on_delete=models.CASCADE)

    class Meta(Grant.Meta):
        constraints = Grant.Meta.constraints + [
            models.UniqueConstraint(fields=["user", "site"], name="registre_site_grant")
        ]
