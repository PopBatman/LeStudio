"""Render one authenticated, immutable Studio composition through Wagtail."""
import base64
import binascii
import json
import re
from functools import lru_cache
from hashlib import sha256
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from uuid import UUID

from django.conf import settings
from django.core.exceptions import RequestDataTooBig
from django.db import DatabaseError
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from wagtail import __version__ as wagtail_version

from .editorial import scoped_public_article
from .models import ReferencePage


ROOT = Path(__file__).parent
FORMATS = ('desktop', 'tablet', 'mobile')
DEFAULTS = dict(accent='#304860', background='#ffffff', ink='#202020', gap=0, font='system')
PROPS = {
    'heading': {'level', 'text'}, 'text': {'text'}, 'signature': {'text'}, 'container': {'layout'},
    'image': {'media', 'alt'}, 'button': {'label', 'url'}, 'article': {'content'},
}
TOKEN_NAMES = set(DEFAULTS)
MAX_HTML = 7 * 1024 * 1024
ASSET_PNG = 'c82f87e90c485351da7b318b1a7f514d060c09799e42d6a9febddaf810861087'


class Refused(ValueError):
    def __init__(self, status=422, code='incompatible'):
        self.status = status
        self.code = code


def require(condition):
    if not condition:
        raise Refused()


def fields(value, required, optional=()):
    require(isinstance(value, dict) and set(required) <= value.keys() <= set(required).union(optional))


def uid(value):
    require(isinstance(value, str) and str(UUID(value)) == value)
    return value


def integer(value, low, high):
    require(type(value) is int and low <= value <= high)
    return value


def string(value, limit=4000):
    require(isinstance(value, str) and len(value) <= limit)
    return value


def digest(data):
    return sha256(data).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False, ensure_ascii=False).encode()


def distinct(pairs):
    obj = dict(pairs)
    require(len(obj) == len(pairs))
    return obj


@lru_cache(maxsize=1)
def renderer_digest():
    paths = [Path(__file__), ROOT/'assets/preview.css', *sorted((ROOT/'templates/reference').glob('*.html'))]
    return digest(b''.join(p.read_bytes() for p in paths))


class RichTextCheck(HTMLParser):
    """Permit the native static rich text subset before any Wagtail expansion."""
    tags = {'p', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'b', 'em', 'i', 'ol', 'ul', 'li',
            'br', 'hr', 'blockquote', 'sup', 'sub', 'code', 'del'}

    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_starttag(self, tag, attrs):
        require(tag in self.tags and all(name == 'data-block-key' for name, value in attrs))
        self.parts.append(f'<{tag}>')

    def handle_endtag(self, tag):
        require(tag in self.tags)
        if tag not in ('hr', 'br'):
            self.parts.append(f'</{tag}>')

    def handle_data(self, data):
        self.parts.append(escape(data))

    def handle_comment(self, data):
        raise Refused()

    def handle_decl(self, decl):
        raise Refused()



def reference_key(ref):
    require(ref['scope'] in ('global', 'site') and re.fullmatch('[a-z][a-z0-9-]{0,63}', ref['key']))
    return ref['scope'], ref['key'], integer(ref['version'], 1, 2147483647)


def appearance(tokens):
    require(not set(tokens) - TOKEN_NAMES)
    values = {**DEFAULTS, **tokens}
    for key in ('accent', 'background', 'ink'):
        require(re.fullmatch('#[0-9a-fA-F]{6}', values[key]))
    require(values['font'] in ('system', 'dm-sans'))
    font = '"DM Sans",sans-serif' if values['font'] == 'dm-sans' else 'system-ui,sans-serif'
    return (f"--accent:{values['accent']};--paper:{values['background']};color:{values['ink']};"
            f"background-color:{values['background']};font-family:{font};gap:{integer(values['gap'], 0, 128)}px;")


def layout_css(layout, fmt, reserved):
    fields(layout, {'base'}, {'tablet', 'mobile'})
    for rule in layout.values():
        fields(rule, (), {'gap', 'columns', 'display'})
    base = layout['base']
    rules = {**base, **layout.get(fmt, {})}
    require(rules.get('display', 'stack') in ('stack', 'grid'))
    display = 'grid' if rules.get('display') == 'grid' else 'flex'
    cols = integer(rules.get('columns', 1), 1, 12)
    gap = f"gap:{integer(rules['gap'], 0, 128)}px;" if 'gap' in rules else ''
    return (f'display:{display};flex-direction:column;grid-template-columns:repeat({cols},minmax(0,1fr));'
            f'min-height:{reserved}px;{gap}')


def placement(block, fmt):
    rules = block.get('placement', {})
    fields(rules, (), {'base', 'tablet', 'mobile'})
    for rule in rules.values():
        fields(rule, (), {'mode', 'x', 'y', 'width', 'height', 'span', 'z'})
    base = rules.get('base', {})
    local = rules.get(fmt, {})
    base_mode = base.get('mode', 'flow')
    mode = local.get('mode', base_mode)
    values = {**(base if base_mode == mode else {}), **local}
    require(mode in ('flow', 'free'))
    return mode, values


def place_css(block, fmt):
    mode, values = placement(block, fmt)
    if mode == 'free':
        x = integer(values['x'], 0, 99)
        y = integer(values['y'], 0, 4095)
        width = integer(values['width'], 1, 100-x)
        height = integer(values['height'], 1, 4096)
        z = integer(values.get('z', 0), 0, 100)
        return f'position:absolute;left:{x}%;top:{y}px;width:{width}%;height:{height}px;z-index:{z};'
    span = integer(values.get('span', 1), 1, 12)
    width = f"{integer(values['width'], 1, 100)}%" if 'width' in values else 'auto'
    height = f"{integer(values['height'], 1, 4096)}px" if 'height' in values else 'auto'
    return f'position:relative;width:{width};height:{height};grid-column:span {span};'


class Composition:
    def __init__(self, payload):
        self.payload = payload
        self.document = payload['document']
        fields(self.document, {'schema_version', 'pages', 'menus', 'theme'})
        self.schema = integer(self.document['schema_version'], 1, 4)
        self.theme = self.document['theme']
        allowed = TOKEN_NAMES | {'media', 'components'} if self.schema >= 3 else {'accent', 'gap'}
        fields(self.theme, (), allowed)
        require(self.schema >= 2 or self.document['menus'] == [])
        require(len(self.theme.get('components', [])) <= 100)
        for setting in self.theme.get('components', []):
            fields(setting, {'definition'}, {'variant', 'tokens'})
            reference_key(setting['definition'])
        require(len(payload['definitions']) <= 2000)
        for definition in payload['definitions']:
            fields(definition, {'scope', 'key', 'version', 'renderer'})
        self.styles = [(ROOT/'assets/preview.css').read_text()]
        self.responsive = {fmt: [] for fmt in FORMATS}
        self.fonts = {}
        self.definitions = {reference_key(d): d for d in payload['definitions']}
        self.used = set()
        self.articles = {}
        self.media = {}
        self.blocks = []
        self.ids = set()
        self.html_budget = MAX_HTML
        self.pages = {uid(p['id']): p for p in self.document['pages']}
        require(0 < len(self.pages) == len(self.document['pages']) <= 100)
        require(len(self.definitions) == len(payload['definitions']))

    def remember(self, node):
        key = uid(node['id'])
        require(key not in self.ids and len(self.ids) < 3000)
        self.ids.add(key)
        return '#n' + key

    def tokens(self, selector, tokens):
        self.styles.append(selector + '{' + appearance(tokens) + '}')
        if tokens.get('font') == 'dm-sans' and not self.fonts:
            font = (ROOT/'assets/dm-sans-latin.woff2').read_bytes()
            self.fonts['dm-sans'] = digest(font)
            encoded = base64.b64encode(font).decode('ascii')
            self.styles.append('@font-face{font-family:"DM Sans";font-weight:100 1000;src:url(data:font/woff2;base64,'
                               + encoded + ') format("woff2")}')

    def container(self, selector, rules, children):
        for screen in FORMATS:
            fmt = 'base' if screen == 'desktop' else screen
            reserved = 0
            for child in children:
                mode, params = placement(child, fmt)
                if mode == 'free':
                    reserved = max(reserved, integer(params['y'], 0, 4095) + integer(params['height'], 1, 4096))
            self.responsive[screen].append(selector + '{' + layout_css(rules, fmt, reserved) + '}')

    def image(self, ref):
        fields(ref, {'kind', 'ref_id'})
        require(ref['kind'] == 'media')
        key = uid(ref['ref_id'])
        item = self.payload['media'][key]
        fields(item, {'sha256', 'data'})
        require(item['sha256'] == ASSET_PNG)
        encoded = item['data']
        self.html_budget -= len(encoded)
        require(self.html_budget > 0 and digest(base64.b64decode(encoded, validate=True)) == ASSET_PNG)
        self.media[key] = ASSET_PNG
        return 'data:image/png;base64,' + encoded

    def article(self, ref):
        fields(ref, {'kind', 'ref_id'})
        require(ref['kind'] == 'wagtail_content')
        key = uid(ref['ref_id'])
        if key not in self.articles:
            coordinates = self.payload['articles'][key]
            fields(coordinates, {'page_id', 'published_revision_id'})
            page = scoped_public_article(integer(coordinates['page_id'], 1, 2147483647))
            if page is None:
                raise Refused(404, 'inaccessible')
            if str(page.live_revision_id) != coordinates['published_revision_id']:
                raise Refused(409, 'content_changed')
            obj = page.live_revision.as_object()
            require(len(obj.body) <= 131072)
            parser = RichTextCheck()
            parser.feed(obj.body)
            parser.close()
            obj.body = ''.join(parser.parts)
            self.articles[key] = obj
        obj = self.articles[key]
        self.html_budget -= len(obj.body.encode('utf-8'))
        require(self.html_budget > 0)
        return obj

    def block(self, block, depth=1):
        require(depth <= 12)
        optional = {'appearance', 'placement'} if self.schema == 4 else {'appearance'} if self.schema == 3 else set()
        fields(block, {'id', 'definition', 'props', 'children'}, optional)
        fields(block['definition'], {'scope', 'key', 'version'})
        fields(block.get('appearance', {}), (), {'variant', 'tokens'})
        selector = self.remember(block)
        self.blocks.append(block['id'])
        key = reference_key(block['definition'])
        renderer = self.definitions[key]['renderer']
        require(renderer in PROPS)
        fields(block['props'], PROPS[renderer])
        self.used.add(key)
        props, children = block['props'], block['children']
        require(isinstance(children, list) and (not children or renderer == 'container'))
        settings_ = next((s for s in self.theme.get('components', []) if s['definition'] == block['definition']), {})
        specific = block.get('appearance', {})
        variant = specific.get('variant', settings_.get('variant', 'primary' if renderer == 'button' else 'default'))
        require(variant in (('primary', 'secondary') if renderer == 'button' else ('default',)))
        self.tokens(selector, {**self.base_tokens, **settings_.get('tokens', {}), **specific.get('tokens', {})})
        for screen in FORMATS:
            self.responsive[screen].append(selector + '{' + place_css(block, 'base' if screen == 'desktop' else screen) + '}')
        result = dict(id=block['id'], renderer=renderer, props=props, variant=variant)
        if renderer in ('heading', 'text', 'signature'):
            string(props['text'])
            if renderer == 'heading':
                integer(props['level'], 1, 6)
        elif renderer == 'button':
            string(props['label'], 120)
            require(string(props['url'], 2048).startswith('https://'))
        elif renderer == 'image':
            string(props['alt'], 300)
            result['src'] = self.image(props['media'])
        elif renderer == 'article':
            result['article'] = self.article(props['content'])
        else:
            self.container(selector, props['layout'], children)
            result['children'] = [self.block(child, depth + 1) for child in children]
        return result

    def menus(self):
        menus = []
        require(len(self.document['menus']) <= 20)
        count = 0
        for menu in self.document['menus']:
            fields(menu, {'id', 'label', 'items'})
            count += len(menu['items'])
            require(count <= 500)
            self.remember(menu)
            nodes = {item['id']: dict(item, children=[]) for item in menu['items']}
            require(len(nodes) == len(menu['items']))
            roots = []
            for item in nodes.values():
                fields(item, {'id', 'label', 'parent_id', 'target', 'visibility', 'children'})
                selector = self.remember(item)
                string(item['label'], 120)
                target = item['target']
                kind = target['kind']
                require(kind in ('page', 'external', 'group'))
                fields(target, {'kind'} | {'page': {'page_id'}, 'external': {'url'}, 'group': set()}[kind])
                if target['kind'] == 'page':
                    require(target['page_id'] in self.pages)
                screens = set(item['visibility'])
                require(screens and screens <= set(FORMATS))
                for fmt in FORMATS:
                    if fmt not in screens:
                        self.responsive[fmt].append(selector + '{display:none}')
                ancestor = item['parent_id']
                parent = ancestor
                for _ in range(6):
                    if ancestor is None:
                        break
                    ancestor = nodes[ancestor]['parent_id']
                require(ancestor is None)
                (roots if parent is None else nodes[parent]['children']).append(item)
            menus.append({'label': string(menu['label'], 120), 'items': roots})
        return menus

    def render(self, request, reference, envelope_hash):
        page = self.pages[self.payload['page_id']]
        fields(page, {'id', 'slug', 'parent_id', 'title', 'sections'})
        self.base_tokens = {k: v for k, v in self.theme.items() if k in TOKEN_NAMES}
        self.tokens('body', self.base_tokens)
        cover = self.image(self.theme['media']) if 'media' in self.theme else None
        sections = []
        for section in page['sections']:
            fields(section, {'id', 'layout', 'blocks'})
            self.container(self.remember(section), section['layout'], section['blocks'])
            sections.append(dict(id=section['id'], blocks=[self.block(b) for b in section['blocks']]))
        menus = self.menus()
        require(self.used == self.definitions.keys() and self.media.keys() == self.payload['media'].keys()
                and self.articles.keys() == self.payload['articles'].keys())
        queries = {'desktop': '(min-width:1024px)', 'tablet': '(min-width:768px) and (max-width:1023.98px)',
                   'mobile': '(max-width:767.98px)'}
        for fmt, css in self.responsive.items():
            self.styles.append('@media ' + queries[fmt] + '{' + ''.join(css) + '}')
        css = '\n'.join(self.styles)
        request.studio_composition = dict(page={'title': string(page['title'], 120), 'sections': sections},
                                          menus=menus, cover=cover, css=css)
        response = reference.serve_preview(request, 'studio_composition')
        require(len(response.content) < MAX_HTML)
        result = {k: self.payload[k] for k in ('site_id', 'instance_id', 'revision_id', 'revision_number', 'page_id')}
        result.update(sha256=envelope_hash, image_digest=settings.ENGINE_IMAGE_DIGEST, engine_version='1.0.0',
                      wagtail_version=wagtail_version, block_ids=self.blocks, definitions=self.payload['definitions'],
                      articles=self.payload['articles'], media=self.media, html_sha256=digest(response.content),
                      renderer_sha256=renderer_digest(), css_sha256=digest(css.encode()), fonts=self.fonts)
        rendered = JsonResponse({'html': response.content.decode(), 'manifest': result}, json_dumps_params={'ensure_ascii': False})
        require(len(rendered.content) <= 8 * 1024 * 1024)
        return rendered


@never_cache
@require_POST
def preview(request):
    if not settings.ENGINE_PREVIEW_ENABLED:
        return JsonResponse({'status': 'inaccessible'}, status=404)
    try:
        require(request.content_type == 'application/json')
        raw = request.body
        require(len(raw) <= 4 * 1024 * 1024)
        envelope = json.loads(raw, object_pairs_hook=distinct)
        payload = envelope['payload']
        require(set(envelope) == {'payload', 'sha256'} and set(payload) == {
            'site_id', 'instance_id', 'revision_id', 'revision_number', 'page_id', 'document', 'definitions', 'articles', 'media'})
        fingerprint = digest(canonical(payload))
        require(fingerprint == envelope['sha256'])
        for key in ('site_id', 'instance_id', 'revision_id', 'page_id'):
            uid(payload[key])
        integer(payload['revision_number'], 1, 2**63-1)
        if (payload['site_id'], payload['instance_id']) != (settings.STUDIO_SITE_ID, settings.ENGINE_INSTANCE_ID):
            raise Refused(404, 'inaccessible')
        ref = ReferencePage.objects.live().get(site_id=payload['site_id'], instance_id=payload['instance_id'],
                                               live_revision__isnull=False)
        return Composition(payload).render(request, ref, fingerprint)
    except Refused as error:
        return JsonResponse({'status': error.code}, status=error.status)
    except (ValueError, KeyError, TypeError, AttributeError, RecursionError, binascii.Error, RequestDataTooBig):
        return JsonResponse({'status': 'incompatible'}, status=422)
    except (ReferencePage.DoesNotExist, ReferencePage.MultipleObjectsReturned, DatabaseError):
        return JsonResponse({'status': 'unavailable'}, status=503)
