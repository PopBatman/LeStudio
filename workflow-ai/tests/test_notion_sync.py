import importlib.util
import json
from pathlib import Path
import tempfile
import sqlite3
import subprocess
import sys
import unittest
import urllib.error

MODULE = Path(__file__).resolve().parents[1] / 'integrations/notion/sync.py'
SPEC = importlib.util.spec_from_file_location('notion_sync', MODULE)
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)

PARENT = '11111111-1111-4111-8111-111111111111'
PAGE = '22222222-2222-4222-8222-222222222222'


class NotionContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'workflow-ai'
        self.root.mkdir()
        (self.root / 'docs').mkdir()
        (self.root / 'docs/spec.md').write_text('# Spec\n\nApproved in Git, not Notion.\n', encoding='utf-8')
        self.manifest = self.root / 'manifest.json'
        self.config = {'schema_version': 1, 'documents': [
            {'id': 'studio-spec', 'title': 'Studio Spec', 'path': 'docs/spec.md'}
        ]}
        self.save()

    def save(self):
        self.manifest.write_text(json.dumps(self.config), encoding='utf-8')

    def test_curated_document_is_projected_with_source_hash(self):
        docs = sync.load_documents(self.root, self.manifest)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]['id'], 'studio-spec')
        self.assertIn('Source SHA256:', docs[0]['markdown'])

    def test_sibling_product_and_workflow_use_their_own_sources(self):
        studio = self.root.parent / 'studio'
        (studio / 'docs').mkdir(parents=True)
        (studio / 'docs/spec.md').write_text('Product specification', encoding='utf-8')
        self.config['documents'][0].update(scope='studio')
        self.config['documents'].append({'id': 'workflow-spec', 'title': 'Workflow',
                                        'path': 'docs/spec.md', 'scope': 'workflow-ai'})
        self.save()
        product_doc, workflow_doc = sync.load_documents(self.root, self.manifest)
        self.assertIn('Product specification', product_doc['markdown'])
        self.assertNotIn('Product specification', workflow_doc['markdown'])
        self.assertEqual(product_doc['id'], 'studio-spec')
        self.assertEqual(product_doc['path'], 'studio/docs/spec.md')
        self.assertEqual(workflow_doc['path'], 'workflow-ai/docs/spec.md')

    def test_product_scope_refuses_symlinked_root_and_unknown_scopes(self):
        (self.root.parent / 'studio').symlink_to(self.root, target_is_directory=True)
        for scope in ('studio', 'another-project'):
            with self.subTest(scope=scope):
                self.config['documents'][0].update(scope=scope)
                self.save()
                with self.assertRaises(ValueError):
                    sync.load_documents(self.root, self.manifest)

    def test_traversal_is_refused(self):
        self.config['documents'][0]['path'] = '../private.md'
        self.save()
        with self.assertRaises(ValueError):
            sync.load_documents(self.root, self.manifest)

    def test_symlink_is_refused(self):
        (self.root / 'docs/alias.md').symlink_to(self.root / 'docs/spec.md')
        self.config['documents'][0]['path'] = 'docs/alias.md'
        self.save()
        with self.assertRaises(ValueError):
            sync.load_documents(self.root, self.manifest)

    def test_unlisted_documents_are_not_read(self):
        (self.root / 'docs/private.md').write_text('PRIVATE', encoding='utf-8')
        docs = sync.load_documents(self.root, self.manifest)
        self.assertEqual(len(docs), 1)
        self.assertNotIn('PRIVATE', json.dumps(docs))

    def test_idempotent_run_does_not_duplicate_page(self):
        class FakeClient:
            def __init__(self): self.calls = []
            def create_page(self, payload):
                self.calls.append(payload)
                return {'id': PAGE, 'parent': {'page_id': PARENT}, 'object': 'page'}
        client = FakeClient()
        docs = sync.load_documents(self.root, self.manifest)
        state = self.root / 'state.sqlite3'
        sync.project(docs, PARENT, state, client)
        sync.project(docs, PARENT, state, client)
        self.assertEqual(len(client.calls), 1)

    def test_changed_document_creates_revision_without_editing_previous(self):
        calls = []
        class Client:
            def create_page(self, payload):
                calls.append(payload)
                return {'id': PAGE, 'parent': {'page_id': PARENT}, 'object': 'page'}
        state = self.root / 'state.sqlite3'
        sync.project(sync.load_documents(self.root, self.manifest), PARENT, state, Client())
        (self.root / 'docs/spec.md').write_text('# Spec\n\nChanged requirement.', encoding='utf-8')
        sync.project(sync.load_documents(self.root, self.manifest), PARENT, state, Client())
        self.assertEqual(len(calls), 2)
        self.assertNotEqual(calls[0]['markdown'], calls[1]['markdown'])

    def test_ambiguous_failure_blocks_resend_even_if_source_changes(self):
        calls = []
        class Client:
            def create_page(self, payload):
                calls.append(payload)
                raise TimeoutError('network unavailable')
        state = self.root / 'state.sqlite3'
        with self.assertRaises(sync.AmbiguousWrite):
            sync.project(sync.load_documents(self.root, self.manifest), PARENT, state, Client())
        (self.root / 'docs/spec.md').write_text('Changed after uncertain write', encoding='utf-8')
        with self.assertRaises(sync.AmbiguousWrite):
            sync.project(sync.load_documents(self.root, self.manifest), PARENT, state, Client())
        self.assertEqual(len(calls), 1)

    def test_partial_batch_does_not_resend_completed_document(self):
        (self.root / 'docs/two.md').write_text('Second', encoding='utf-8')
        self.config['documents'].append({'id': 'studio-two', 'title': 'Second', 'path': 'docs/two.md'})
        self.save()
        calls = []
        class Client:
            def create_page(self, payload):
                calls.append(payload)
                if len(calls) == 2: raise TimeoutError()
                return {'id': PAGE, 'parent': {'page_id': PARENT}, 'object': 'page'}
        state = self.root / 'state.sqlite3'
        docs = sync.load_documents(self.root, self.manifest)
        with self.assertRaises(sync.AmbiguousWrite): sync.project(docs, PARENT, state, Client())
        with self.assertRaises(sync.AmbiguousWrite): sync.project(docs, PARENT, state, Client())
        self.assertEqual(len(calls), 2)

    def test_reconcile_verifies_parent_and_projection_marker(self):
        docs = sync.load_documents(self.root, self.manifest)
        class Client:
            def create_page(self, payload): raise TimeoutError()
            def get_page(self, page_id): return {'id': page_id, 'object': 'page', 'parent': {'page_id': PARENT}}
            def get_markdown(self, page_id): return {'markdown': docs[0]['markdown'], 'truncated': False}
        state = self.root / 'state.sqlite3'
        with self.assertRaises(sync.AmbiguousWrite): sync.project(docs, PARENT, state, Client())
        result = sync.reconcile('studio-spec', PAGE, PARENT, state, Client())
        self.assertEqual(result['status'], 'reconciled')
        self.assertEqual(sync.project(docs, PARENT, state, Client())[0]['status'], 'unchanged')

    def test_reconcile_wrong_page_is_refused(self):
        docs = sync.load_documents(self.root, self.manifest)
        class Client:
            def create_page(self, payload): raise TimeoutError()
            def get_page(self, page_id): return {'id': page_id, 'object': 'page', 'parent': {'page_id': PARENT}}
            def get_markdown(self, page_id): return {'markdown': 'unrelated user content'}
        state = self.root / 'state.sqlite3'
        with self.assertRaises(sync.AmbiguousWrite): sync.project(docs, PARENT, state, Client())
        with self.assertRaises(sync.SyncError): sync.reconcile('studio-spec', PAGE, PARENT, state, Client())

    def test_rate_limited_write_is_not_retried_before_retry_after(self):
        calls = []
        class Client:
            def create_page(self, payload):
                calls.append(payload)
                raise sync.RejectedWrite(429, retry_after=120)
        state = self.root / 'state.sqlite3'
        docs = sync.load_documents(self.root, self.manifest)
        with self.assertRaises(sync.RejectedWrite): sync.project(docs, PARENT, state, Client())
        with self.assertRaises(sync.SyncError): sync.project(docs, PARENT, state, Client())
        self.assertEqual(len(calls), 1)

    def test_different_targets_are_not_mistaken_for_same_projection(self):
        calls = []
        class Client:
            def create_page(self, payload):
                calls.append(payload)
                return {'id': PAGE, 'object': 'page', 'parent': payload['parent']}
        docs = sync.load_documents(self.root, self.manifest)
        state = self.root / 'state.sqlite3'
        sync.project(docs, PARENT, state, Client())
        sync.project(docs, PAGE, state, Client())
        self.assertEqual(len(calls), 2)

    def test_hidden_file_duplicate_id_and_oversized_file_refused(self):
        for relative in ('.env', '.private/spec.md', '/etc/passwd', '../outside.md'):
            self.config['documents'][0]['path'] = relative
            self.save()
            with self.assertRaises(ValueError): sync.load_documents(self.root, self.manifest)
        self.config['documents'][0]['path'] = 'docs/spec.md'
        self.config['documents'].append(dict(self.config['documents'][0]))
        self.save()
        with self.assertRaises(ValueError): sync.load_documents(self.root, self.manifest)
        self.config['documents'] = self.config['documents'][:1]
        self.save()
        (self.root / 'docs/spec.md').write_bytes(b'x' * (sync.MAX_DOCUMENT_BYTES + 1))
        with self.assertRaises(ValueError): sync.load_documents(self.root, self.manifest)

    def test_markdown_xml_and_external_assets_become_plain_links(self):
        (self.root / 'docs/spec.md').write_text('<page url="https://example.com">X</page>\n\n![img](https://example.com/a.png)', encoding='utf-8')
        doc = sync.load_documents(self.root, self.manifest)[0]
        self.assertIn('\\<page', doc['markdown'])
        self.assertNotIn('![img]', doc['markdown'])

    def test_dry_run_needs_no_credentials_and_creates_no_state(self):
        result = subprocess.run([sys.executable, str(MODULE), '--root', str(self.root), '--manifest', str(self.manifest),
                                 '--state', str(self.root / 'state.sqlite3'), '--dry-run'],
                                text=True, capture_output=True, env={})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['network_calls'], 0)
        self.assertFalse((self.root / 'state.sqlite3').exists())

    def test_untrusted_origin_and_redirects_refused(self):
        client = sync.NotionClient('test-token')
        with self.assertRaises(ValueError): client._request('GET', 'https://evil.test/v1/pages')
        self.assertIsNone(sync.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://evil.test/'))

    def test_503_post_is_ambiguous_without_retry_and_token_omitted(self):
        calls = []
        class Opener:
            def open(self, request, timeout):
                calls.append(request)
                raise urllib.error.HTTPError(request.full_url, 503, 'secret-response', {}, None)
        client = sync.NotionClient('never-print-this-token', opener=Opener())
        with self.assertRaises(sync.AmbiguousWrite) as raised: client.create_page({})
        self.assertEqual(len(calls), 1)
        self.assertNotIn('never-print-this-token', str(raised.exception))
        self.assertNotIn('secret-response', str(raised.exception))

    def test_active_lock_prevents_second_writer(self):
        state = self.root / 'state.sqlite3'
        with sync.ledger(state):
            with self.assertRaises(sync.SyncError):
                with sync.ledger(state): pass


if __name__ == '__main__':
    unittest.main()
