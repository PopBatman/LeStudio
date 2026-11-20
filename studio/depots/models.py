from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone


class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    site = models.ForeignKey("registre.Site", on_delete=models.PROTECT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    secret_digest = models.CharField(max_length=64, unique=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(db_index=True)
    revoked_at = models.DateTimeField(null=True)
    last_version = models.PositiveIntegerField(default=0)

    @property
    def active(self):
        return self.revoked_at is None and timezone.now() < self.expires_at


class PortalSession(models.Model):
    digest = models.CharField(max_length=64, primary_key=True)
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE)
    expires_at = models.DateTimeField(db_index=True)


class ExchangeWindow(models.Model):
    address_digest = models.CharField(max_length=64, primary_key=True)
    started_at = models.DateTimeField(db_index=True)
    attempts = models.PositiveSmallIntegerField(default=0)


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    invitation = models.ForeignKey(Invitation, on_delete=models.PROTECT)
    version = models.PositiveIntegerField()
    request_id = models.UUIDField()
    figma_url = models.CharField(max_length=2048)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    erased_at = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["invitation", "version"], name="depot_invitation_version"),
            models.UniqueConstraint(fields=["invitation", "request_id"], name="depot_invitation_request"),
            models.CheckConstraint(condition=models.Q(version__gte=1), name="depot_positive_version"),
        ]


class ImportAnalysis(models.Model):
    """A private review of one submission; retain its local receipt after source erasure."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    submission = models.OneToOneField(Submission, null=True, on_delete=models.SET_NULL)
    token = models.UUIDField(default=uuid4)
    state = models.CharField(max_length=16, default="loading")
    generation = models.CharField(max_length=128, blank=True)
    version = models.CharField(max_length=128, blank=True)
    rules_version = models.PositiveSmallIntegerField(default=1)
    base_revision = models.ForeignKey("composition.CompositionRevision", null=True,
                                      related_name="+", on_delete=models.PROTECT)
    result_revision = models.OneToOneField("composition.CompositionRevision", null=True,
                                          related_name="+", on_delete=models.PROTECT)
    inventory = models.JSONField(default=dict)
    observation = models.JSONField(default=dict)
    proposals = models.JSONField(default=list)
    decisions = models.JSONField(default=dict)
    destinations = models.JSONField(default=list)
    mapping = models.JSONField(default=dict)
    error = models.CharField(max_length=256, blank=True)
    retry_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)


class FrameReference(models.Model):
    """Normalized private PNG and the operator's declaration about its origin."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    analysis = models.ForeignKey(ImportAnalysis, on_delete=models.CASCADE)
    page_id = models.UUIDField()
    frame_id = models.CharField(max_length=128)
    version = models.CharField(max_length=128)
    format = models.CharField(max_length=8)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    digest = models.CharField(max_length=64)
    # Keep historical metadata for decisions. Only the current reference has image bytes.
    png = models.BinaryField(null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("analysis", "frame_id"),
                       condition=models.Q(png__isnull=False), name="comparison_one_current_png")]


class ComparisonDecision(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    reference = models.ForeignKey(FrameReference, on_delete=models.CASCADE)
    revision = models.ForeignKey("composition.CompositionRevision", on_delete=models.PROTECT)
    page_id = models.UUIDField()
    target = models.UUIDField(null=True)
    kind = models.CharField(max_length=12)
    note = models.CharField(max_length=1000)
    width = models.PositiveIntegerField()
    instance_id = models.UUIDField()
    render_digest = models.CharField(max_length=64)
    key = models.UUIDField()
    previous = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("reference", "author", "key"),
                                              name="comparison_decision_retry")]
        ordering = ("-created_at", "-pk")
