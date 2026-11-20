from django.conf import settings
from django.db import models


class SiteConnection(models.Model):
    site = models.OneToOneField("registre.Site", primary_key=True, on_delete=models.PROTECT)
    instance_id = models.UUIDField(unique=True, null=True)
    confirmed_profile = models.CharField(max_length=100, blank=True)
    confirmed_at = models.DateTimeField(null=True)
    versions = models.JSONField(default=dict)

    attempt_id = models.UUIDField()
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    started_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True)
    diagnostic = models.CharField(max_length=64, default="checking")
