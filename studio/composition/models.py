from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class CompositionRevision(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    site = models.ForeignKey("registre.Site", on_delete=models.PROTECT)
    number = models.PositiveBigIntegerField()
    parent = models.ForeignKey("self", null=True, on_delete=models.PROTECT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    origin = models.JSONField(null=True)
    document = models.JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["site", "number"], name="composition_site_revision"),
            models.CheckConstraint(
                condition=(
                    Q(number=1, parent__isnull=True, origin__isnull=False)
                    | Q(number__gt=1, parent__isnull=False, origin__isnull=True)
                ),
                name="composition_revision_lineage",
            ),
        ]

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self._state.adding or force_update or update_fields is not None:
            raise ValidationError("Une révision enregistrée est immuable.")
        return super().save(force_insert=True, using=using)


class ComponentVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    site = models.ForeignKey("registre.Site", null=True, on_delete=models.PROTECT)
    key = models.SlugField(max_length=64)
    version = models.PositiveIntegerField()
    label = models.CharField(max_length=120)
    renderer = models.CharField(max_length=64)
    manifest = models.JSONField()
    origin = models.CharField(max_length=20)
    retired = models.BooleanField(default=False)

    class Meta:
        ordering = ["label", "key", "version", "pk"]
        constraints = [
            models.UniqueConstraint(fields=["key", "version"], condition=Q(site__isnull=True),
                                    name="catalogue_global_version"),
            models.UniqueConstraint(fields=["site", "key", "version"], condition=Q(site__isnull=False),
                                    name="catalogue_site_version"),
            models.CheckConstraint(condition=Q(version__gte=1), name="catalogue_version_positive"),
            models.CheckConstraint(condition=(Q(site__isnull=False, origin="sur_mesure")
                                              | Q(site__isnull=True, origin__in=["standard", "promotion_revue"])),
                                   name="catalogue_version_origin"),
        ]

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self._state.adding or force_update or update_fields is not None:
            raise ValidationError("Une version de composant enregistrée est immuable.")
        return super().save(force_insert=True, using=using)


class SiteMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    site = models.ForeignKey("registre.Site", on_delete=models.PROTECT)
    asset = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["site", "asset"], name="catalogue_site_asset")]


class Promotion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    source = models.ForeignKey(ComponentVersion, on_delete=models.PROTECT, related_name="proposals")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    key = models.SlugField(max_length=64)
    version = models.PositiveIntegerField()
    label = models.CharField(max_length=120)
    rights = models.CharField(max_length=500)
    reason = models.CharField(max_length=500)
    fingerprint = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=12, default="pending")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name="+")
    decided_at = models.DateTimeField(null=True)
    note = models.CharField(max_length=500, blank=True)
    result = models.OneToOneField(ComponentVersion, null=True, on_delete=models.PROTECT, related_name="promotion")

    class Meta:
        constraints = [
            models.CheckConstraint(condition=(Q(state="pending", reviewer__isnull=True, result__isnull=True, decided_at__isnull=True)
                                              | Q(state="accepted", reviewer__isnull=False, result__isnull=False, decided_at__isnull=False)
                                              | Q(state="rejected", reviewer__isnull=False, result__isnull=True, decided_at__isnull=False)),
                                   name="catalogue_promotion_decision"),
            models.CheckConstraint(condition=~Q(reviewer=models.F("author")), name="catalogue_independent_review"),
        ]


class EditorialCoordinates(models.Model):
    site = models.ForeignKey("registre.Site", on_delete=models.PROTECT)
    instance_id = models.UUIDField()
    content_type = models.CharField(max_length=12, default="article", choices=[("article", "Article")])
    page_number = models.PositiveIntegerField()

    class Meta:
        abstract = True


class ReferenceQuerySet(models.QuerySet):
    def update(self, **kwargs):
        raise ValidationError("Ce repère est immuable.")

    def delete(self):
        raise ValidationError("Ce repère appartient à l’historique.")


class EditorialReference(EditorialCoordinates):
    objects = ReferenceQuerySet.as_manager()
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    published_revision = models.CharField(max_length=32)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["site", "instance_id", "content_type", "page_number", "published_revision"],
            name="unique_editorial_reference")]

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise ValidationError("Ce repère est immuable.")
        kwargs["force_insert"] = True
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Ce repère appartient à l’historique.")


class EditorialObservation(EditorialCoordinates):
    id = models.BigAutoField(primary_key=True)
    connection_attempt = models.UUIDField()
    attempt = models.UUIDField(default=uuid4, unique=True)
    status = models.CharField(max_length=16)
    checked_at = models.DateTimeField(null=True)
    last_success_at = models.DateTimeField(null=True)
    published_revision = models.CharField(max_length=32, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["site", "instance_id", "content_type", "page_number"],
            name="unique_editorial_observation")]


class PreviewTicket(models.Model):
    """Short-lived receipt. Rendered HTML, editorial text and assets never enter this table."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    session = models.ForeignKey("sessions.Session", on_delete=models.CASCADE)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    revision = models.ForeignKey(CompositionRevision, on_delete=models.CASCADE)
    page_id = models.UUIDField()
    fingerprint = models.CharField(max_length=64)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField(db_index=True)


class BuilderSave(models.Model):
    """Recorded outcome of one authorized save, including its local occurrence IDs."""
    id = models.BigAutoField(primary_key=True)
    site = models.ForeignKey("registre.Site", on_delete=models.CASCADE)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.UUIDField()
    fingerprint = models.CharField(max_length=64)
    revision = models.ForeignKey(CompositionRevision, on_delete=models.CASCADE)
    mapping = models.JSONField()
    selection = models.UUIDField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("site", "operator", "key"), name="builder_save_scoped_key")
        ]
