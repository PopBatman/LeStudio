from django.db import models
from django.http import HttpResponse
from django.utils.html import format_html
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class ReferencePage(Page):
    site_id = models.UUIDField(editable=False)
    instance_id = models.UUIDField(editable=False)
    marker = models.CharField(max_length=200)

    def serve_preview(self, request, mode_name):
        if mode_name == "studio_composition":
            from django.shortcuts import render
            return render(request, "reference/composition_preview.html", request.studio_composition)
        return super().serve_preview(request, mode_name)

    def serve(self, request, *args, **kwargs):
        html = format_html(
            '<!doctype html><html lang="fr"><meta charset="utf-8">'
            '<title>{}</title><main><p>{}</p></main></html>', self.title, self.marker
        )
        return HttpResponse(html)


class ArticlePage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel("body")]
    subpage_types = []

    class Meta:
        verbose_name = "article"
