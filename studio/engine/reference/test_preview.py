from hashlib import sha256
import json
from uuid import uuid4

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings
from wagtail.models import PageViewRestriction, Revision, Site

from .models import ArticlePage, ReferencePage


def uid():
    return str(uuid4())


@override_settings(ENGINE_PREVIEW_ENABLED=True)
class PreviewTests(TestCase):
    url = '/internal/preview/v1/render'

    @classmethod
    def setUpTestData(cls):
        call_command("seed_reference")

    def setUp(self):
        self.page = {'id': uid(), 'parent_id': None, 'slug': '', 'title': 'Page test', 'sections': []}
        self.block = {'id': uid(), 'definition': {'scope': 'global', 'key': 'heading', 'version': 1},
                      'props': {'text': 'Titre enregistré', 'level': 2}, 'children': []}
        self.page['sections'].append({'id': uid(), 'layout': {'base': {}}, 'blocks': [self.block]})
        self.payload = {'site_id': settings.STUDIO_SITE_ID, 'instance_id': settings.ENGINE_INSTANCE_ID,
                        'revision_id': uid(), 'revision_number': 7, 'page_id': self.page['id'],
                        'document': {'schema_version': 4, 'pages': [self.page], 'theme': {}, 'menus': []},
                        'definitions': [dict(self.block['definition'], renderer='heading')], 'articles': {}, 'media': {}}

    def render(self):
        digest = sha256(json.dumps(self.payload, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
        return self.client.post(self.url, {'payload': self.payload, 'sha256': digest}, content_type='application/json')

    def test_readonly_render_and_compatibility(self):
        before = Revision.objects.count(), ReferencePage.objects.get().live_revision_id
        for schema in range(1, 5):
            self.payload['document']['schema_version'] = schema
            response = self.render()
            self.assertEqual(response.status_code, 200)
            result = response.json()
            self.assertIn('Titre enregistré', result['html'])
            self.assertEqual(result['manifest']['block_ids'], [self.block['id']])
            self.assertEqual(result['manifest']['html_sha256'], sha256(result['html'].encode()).hexdigest())
        self.assertEqual(before, (Revision.objects.count(), ReferencePage.objects.get().live_revision_id))
        self.payload['instance_id'] = uid()
        self.assertEqual(self.render().status_code, 404)
        with self.settings(ENGINE_PREVIEW_ENABLED=False):
            self.assertNotIn('preview.v1', self.client.get('/internal/version').json().get('capabilities', []))
            self.assertEqual(self.render().status_code, 404)

    def test_public_article_exact_revision_and_restrictions(self):
        site = Site.objects.get(is_default_site=True)
        article = site.root_page.add_child(instance=ArticlePage(title='Public', slug='public', body='<p>Éditorial</p>'))
        rev = article.save_revision()
        rev.publish()
        ref = uid()
        self.block.update(definition={'scope': 'site', 'key': 'news', 'version': 2},
                          props={'content': {'kind': 'wagtail_content', 'ref_id': ref}})
        self.payload.update(definitions=[dict(self.block['definition'], renderer='article')],
                            articles={ref: {'page_id': article.pk, 'published_revision_id': str(rev.pk)}})
        with self.settings(EDITORIAL_WAGTAIL_SITE_ID=site.pk):
            self.assertIn('Éditorial', self.render().json()['html'])
            restriction = PageViewRestriction.objects.create(page=site.root_page, restriction_type='login')
            self.assertEqual(self.render().status_code, 404)
            restriction.delete()
            article.title = 'Nouvelle version'
            article.save_revision().publish()
            self.assertEqual(self.render().status_code, 409)

    def test_responsive_tree_menu_and_font(self):
        doc = self.payload['document']
        doc['theme'] = {'font': 'dm-sans'}
        self.block['placement'] = {'base': {'mode': 'free', 'x': 5, 'y': 8, 'width': 40, 'height': 50},
                                   'mobile': {'mode': 'flow'}}
        menu_id = uid()
        doc['menus'] = [{'id': uid(), 'label': 'Navigation', 'items': [
            {'id': menu_id, 'parent_id': None, 'label': 'Accueil', 'target': {'kind': 'page', 'page_id': self.page['id']},
             'visibility': ['mobile']},
        ]}]
        container = {'id': uid(), 'definition': {'scope': 'global', 'key': 'container', 'version': 1},
                     'props': {'layout': {'base': {}, 'tablet': {'display': 'grid', 'columns': 2}}},
                     'children': [self.block]}
        self.page['sections'][0]['blocks'] = [container]
        self.payload['definitions'].append(dict(container['definition'], renderer='container'))
        response = self.render()
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['manifest']['block_ids'], [container['id'], self.block['id']])
        self.assertEqual(len(result['manifest']['fonts']['dm-sans']), 64)
        for text in ('data:font/woff2;base64,', 'left:5%;top:8px', 'repeat(2,minmax', f'#n{menu_id}{{display:none}}',
                     f'data-studio-page-id="{self.page["id"]}"', 'Accueil', 'min-height:58px;'):
            self.assertIn(text, result['html'])

    def test_rejects_unresolved_or_unsupported_dependencies(self):
        self.block['definition']['version'] = 2
        self.assertEqual(self.render().status_code, 422)
        self.block['definition']['version'] = 1
        self.payload['definitions'][0]['renderer'] = 'unknown'
        self.assertEqual(self.render().status_code, 422)
        self.payload['definitions'][0]['renderer'] = 'heading'
        self.payload['document']['theme'] = {'media': {'kind': 'media', 'ref_id': uid()}}
        self.assertEqual(self.render().status_code, 422)
