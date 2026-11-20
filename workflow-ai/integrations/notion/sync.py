#!/usr/bin/env python3
"""Versioned, one-way Notion documentation projection. Python stdlib only."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

API_VERSION = '2026-03-11'
API_ORIGIN = 'https://api.notion.com'
ROOT = Path(__file__).resolve().parents[2]
MAX_DOCUMENT_BYTES = 128 * 1024
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
SLUG = re.compile(r'^[a-z][a-z0-9-]{1,79}$')


class SyncError(Exception):
    """Safe error text; never includes request credentials or response content."""


class AmbiguousWrite(SyncError):
    pass


class RejectedWrite(SyncError):
    def __init__(self, status, retry_after=0):
        self.status = status
        self.retry_after = retry_after
        super().__init__(f'Notion rejected request (HTTP {status}); retry after {retry_after}s.')


def canonical_id(value):
    try:
        return str(uuid.UUID(value))
    except (ValueError, TypeError, AttributeError):
        raise ValueError('A Notion record ID must be a UUID, not a URL.') from None


def sha256(value):
    return hashlib.sha256(value).hexdigest()


def bounded_read(path, maximum):
    with path.open('rb') as handle:
        content = handle.read(maximum + 1)
    if len(content) > maximum:
        raise ValueError('File exceeds the configured size limit.')
    return content


def markdown_data(text):
    """Avoid interpreting external assets or Notion XML control tags in prose."""
    result, fence = [], None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            delim = match.group(1)[0]
            if fence is None:
                fence = delim
            elif delim == fence:
                fence = None
            result.append(line)
        elif fence:
            result.append(line)
        else:
            result.append(line.replace('<', '\\<').replace('![', '['))
    return '\n'.join(result) + '\n'


def load_documents(root, manifest):
    root = Path(root).resolve(strict=True)
    manifest = Path(manifest)
    config = json.loads(bounded_read(manifest, 256 * 1024).decode('utf-8'))
    if not isinstance(config, dict) or config.get('schema_version') != 1:
        raise ValueError('Expected manifest schema_version 1.')
    if set(config) != {'schema_version', 'documents'}:
        raise ValueError('Unexpected manifest keys.')
    entries = config['documents']
    if not isinstance(entries, list) or not 1 <= len(entries) <= 40:
        raise ValueError('Manifest must allowlist between 1 and 40 documents.')
    result, seen_ids, seen_paths = [], set(), set()
    for entry in entries:
        if not isinstance(entry, dict) or not {'id', 'title', 'path'} <= set(entry):
            raise ValueError('Each document needs id, title and path.')
        if set(entry) - {'id', 'title', 'path', 'scope', 'source_url'}:
            raise ValueError('Unexpected document keys.')
        scope = entry.get('scope', 'workflow-ai')
        if scope not in ('workflow-ai', 'studio'):
            raise ValueError('Document scope must be workflow-ai or studio.')
        source_root = root if scope == 'workflow-ai' else root.parent / 'studio'
        if source_root.is_symlink():
            raise ValueError('Symlink source directories are refused.')
        doc_id, title, relative = entry['id'], entry['title'], entry['path']
        if not isinstance(doc_id, str) or not SLUG.fullmatch(doc_id) or doc_id in seen_ids:
            raise ValueError('Document IDs must be unique stable slugs.')
        if not isinstance(title, str) or not title.strip() or len(title) > 160 or any(ord(c) < 32 for c in title):
            raise ValueError('Invalid document title.')
        if not isinstance(relative, str) or '\\' in relative:
            raise ValueError('Use a relative POSIX Markdown path.')
        parts = PurePosixPath(relative).parts
        if (not parts or PurePosixPath(relative).is_absolute() or any(p in {'.', '..'} or p.startswith('.') for p in parts)
                or PurePosixPath(relative).suffix != '.md'):
            raise ValueError('Only non-hidden Markdown files under the root are allowed.')
        path = source_root
        for part in parts:
            path = path / part
            if path.is_symlink():
                raise ValueError('Symlink documents and parent directories are refused.')
        resolved = path.resolve(strict=True)
        if not resolved.is_relative_to(source_root) or not resolved.is_file() or resolved in seen_paths:
            raise ValueError('Source path escapes root, is duplicated, or is not a file.')
        source = bounded_read(resolved, MAX_DOCUMENT_BYTES).decode('utf-8')
        if '\x00' in source:
            raise ValueError('Document contains binary content.')
        url = entry.get('source_url', '')
        if url:
            if not isinstance(url, str) or len(url) > 2000:
                raise ValueError('Invalid source_url.')
            parsed = urllib.parse.urlsplit(url)
            if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or '\n' in url or '\r' in url:
                raise ValueError('source_url must be an HTTPS URL without credentials.')
        content_hash = sha256(source.encode('utf-8'))
        if 'scope' in entry:
            relative = f'{scope}/{relative}'
        identity = json.dumps({'id': doc_id, 'title': title, 'path': relative, 'source_url': url,
                               'source_hash': content_hash, 'renderer': 1, 'api': API_VERSION}, sort_keys=True)
        digest = sha256(identity.encode('utf-8'))
        header = (f'Projection Workspace AI — {doc_id}\n\n'
                  f'Source: `{relative}`\n\nSource SHA256: `{content_hash}`\n\n'
                  f'Projection SHA256: `{digest}`\n\n'
                  'Copie de consultation. Les décisions et autorisations restent dans le dépôt source.\n\n')
        if url:
            header += f'Source canonique: {url}\n\n'
        markdown = header + '---\n\n' + markdown_data(source)
        result.append({'id': doc_id, 'title': title, 'path': relative, 'source_sha256': content_hash,
                       'projection_sha256': digest, 'markdown': markdown})
        seen_ids.add(doc_id)
        seen_paths.add(resolved)
    return result


def page_payload(document, parent_id):
    return {'parent': {'page_id': canonical_id(parent_id)},
            'properties': {'title': {'type': 'title', 'title': [
                {'type': 'text', 'text': {'content': document['title'] + ' · ' + document['projection_sha256'][:10]}}
            ]}}, 'markdown_version': 'v2', 'markdown': document['markdown']}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class NotionClient:
    def __init__(self, token, *, opener=None):
        if not token or len(token) > 4096 or not token.isascii() or any(ord(c) < 33 or ord(c) > 126 for c in token):
            raise ValueError('NOTION_API_TOKEN is absent or invalid.')
        self._token = token
        self._opener = opener or urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())

    def _request(self, method, path, payload=None):
        # No arbitrary endpoints, configurable origins or redirects are accepted.
        if not re.fullmatch(r'/v1/pages(?:/[0-9a-f-]{36}(?:/markdown\?markdown_version=v2)?)?', path):
            raise ValueError('Endpoint is not allowlisted.')
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8') if payload is not None else None
        request = urllib.request.Request(API_ORIGIN + path, data=body, method=method,
            headers={'Authorization': 'Bearer ' + self._token, 'Notion-Version': API_VERSION,
                     'Content-Type': 'application/json', 'User-Agent': 'WorkspaceAI-NotionProjection/0.1'})
        try:
            with self._opener.open(request, timeout=20) as response:
                raw = response.read(MAX_RESPONSE_BYTES + 1)
                if len(raw) > MAX_RESPONSE_BYTES:
                    raise SyncError('Notion response exceeds the size limit.')
                result = json.loads(raw)
                if not isinstance(result, dict):
                    raise SyncError('Notion returned an unexpected response.')
                return result
        except urllib.error.HTTPError as exc:
            status = exc.code
            # A 503 may have committed the POST. Never retry this write automatically.
            if status in {429, 529}:
                value = exc.headers.get('Retry-After', '5')
                retry = int(value) if re.fullmatch(r'\d{1,6}', value) else 60
                raise RejectedWrite(status, max(1, retry)) from None
            if 400 <= status < 500:
                raise RejectedWrite(status) from None
            if method == 'POST':
                raise AmbiguousWrite('Write outcome unknown. Reconcile the pending revision before retrying.') from None
            raise SyncError(f'Notion read failed (HTTP {status}).') from None
        except (OSError, ValueError, SyncError) as exc:
            if method == 'POST':
                raise AmbiguousWrite('Write outcome unknown. Reconcile the pending revision before retrying.') from None
            raise SyncError('Notion read failed; credentials and response content were omitted.') from None

    def create_page(self, payload):
        return self._request('POST', '/v1/pages', payload)

    def get_page(self, page_id):
        return self._request('GET', '/v1/pages/' + canonical_id(page_id))

    def get_markdown(self, page_id):
        return self._request('GET', '/v1/pages/' + canonical_id(page_id) + '/markdown?markdown_version=v2')


@contextmanager
def ledger(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + '.lock')
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise SyncError('Projection already running or stale lock present. Inspect the lock before removing it.') from None
    connection = None
    try:
        os.write(fd, str(os.getpid()).encode('ascii'))
        os.close(fd)
        connection = sqlite3.connect(path, timeout=5)
        os.chmod(path, 0o600)
        connection.row_factory = sqlite3.Row
        connection.execute('''CREATE TABLE IF NOT EXISTS revisions (
            parent TEXT NOT NULL, doc TEXT NOT NULL, digest TEXT NOT NULL,
            status TEXT NOT NULL, page TEXT, retry_at REAL NOT NULL DEFAULT 0,
            PRIMARY KEY(parent, doc, digest))''')
        connection.commit()
        yield connection
    finally:
        if connection:
            connection.close()
        lock.unlink(missing_ok=True)


def _verify_page(page, parent_id):
    if (page.get('object') != 'page' or page.get('archived') or page.get('in_trash')
            or canonical_id(page.get('parent', {}).get('page_id')) != parent_id):
        raise SyncError('Returned page is not active under the configured parent.')
    return canonical_id(page.get('id'))


def project(documents, parent_id, state_path, client):
    parent_id = canonical_id(parent_id)
    reports = []
    with ledger(state_path) as db:
        for document in documents:
            key = (parent_id, document['id'], document['projection_sha256'])
            pending = db.execute("SELECT digest FROM revisions WHERE parent=? AND doc=? AND status='pending'", key[:2]).fetchone()
            if pending:
                raise AmbiguousWrite('Pending revision for ' + document['id'] + '; reconcile before another write.')
            existing = db.execute('SELECT * FROM revisions WHERE parent=? AND doc=? AND digest=?', key).fetchone()
            if existing and existing['status'] == 'complete':
                reports.append({'id': document['id'], 'status': 'unchanged', 'page_id': existing['page']})
                continue
            deferred = db.execute('SELECT MAX(retry_at) FROM revisions WHERE parent=?', (parent_id,)).fetchone()[0]
            if deferred and deferred > time.time():
                raise SyncError('Notion rate limit is still active; wait until the recorded retry time.')
            db.execute("INSERT OR REPLACE INTO revisions(parent,doc,digest,status) VALUES(?,?,?,'pending')", key)
            db.commit()  # durable intent BEFORE the remote effect
            try:
                response = client.create_page(page_payload(document, parent_id))
                page_id = _verify_page(response, parent_id)
            except RejectedWrite as exc:
                db.execute("UPDATE revisions SET status='rejected', retry_at=? WHERE parent=? AND doc=? AND digest=?",
                           (time.time() + exc.retry_after, *key))
                db.commit()
                raise
            except Exception:
                # Includes process/API uncertainty: do not clear intent or silently resend.
                raise AmbiguousWrite('Write outcome unknown for ' + document['id'] + '; reconcile before retrying.') from None
            db.execute("UPDATE revisions SET status='complete', page=?, retry_at=0 WHERE parent=? AND doc=? AND digest=?",
                       (page_id, *key))
            db.commit()
            reports.append({'id': document['id'], 'status': 'created', 'page_id': page_id})
    return reports


def reconcile(doc_id, page_id, parent_id, state_path, client):
    if not SLUG.fullmatch(doc_id):
        raise ValueError('Invalid document ID.')
    parent_id, page_id = canonical_id(parent_id), canonical_id(page_id)
    with ledger(state_path) as db:
        pending = db.execute("SELECT digest FROM revisions WHERE parent=? AND doc=? AND status='pending'",
                             (parent_id, doc_id)).fetchall()
        if len(pending) != 1:
            raise SyncError('Reconciliation needs exactly one pending revision for this document and parent.')
        verified = _verify_page(client.get_page(page_id), parent_id)
        content = client.get_markdown(page_id)
        if content.get('truncated') or content.get('unknown_block_ids'):
            raise SyncError('Cannot reconcile incomplete page content.')
        digest = pending[0]['digest']
        markdown = content.get('markdown', '')
        if (f'Projection SHA256: `{digest}`' not in markdown
                or f'Projection Workspace AI — {doc_id}' not in markdown):
            raise SyncError('Page does not contain the expected projection identity.')
        db.execute("UPDATE revisions SET status='complete',page=? WHERE parent=? AND doc=? AND digest=?",
                   (verified, parent_id, doc_id, digest))
        db.commit()
    return {'id': doc_id, 'status': 'reconciled', 'page_id': verified}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--manifest', type=Path, default=ROOT / 'integrations/notion/config.example.json')
    parser.add_argument('--state', type=Path, default=ROOT / '.workspace/notion.sqlite3')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--dry-run', action='store_true')
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--reconcile', metavar='DOCUMENT_ID')
    parser.add_argument('--page-id')
    parser.add_argument('--export', type=Path, help='Write rendered payloads locally (dry-run only).')
    args = parser.parse_args(argv)
    try:
        if args.export and (args.apply or args.reconcile):
            raise ValueError('--export is only supported in dry-run mode.')
        if args.page_id and not args.reconcile:
            raise ValueError('--page-id is only supported with --reconcile.')
        if args.apply or args.reconcile:
            parent = canonical_id(os.environ.get('NOTION_PARENT_PAGE_ID'))
            client = NotionClient(os.environ.get('NOTION_API_TOKEN', ''))
            if args.reconcile:
                result = reconcile(args.reconcile, args.page_id, parent, args.state, client)
            else:
                documents = load_documents(args.root, args.manifest)
                result = project(documents, parent, args.state, client)
        else:
            documents = load_documents(args.root, args.manifest)
            result = {'mode': 'dry-run', 'network_calls': 0, 'documents': [
                {k: v for k, v in doc.items() if k != 'markdown'} for doc in documents]}
            if args.export:
                # Exclusive creation avoids accidental overwrite of source documents or ledgers.
                with args.export.open('x', encoding='utf-8') as output:
                    json.dump({'api_version': API_VERSION, 'markdown_version': 'v2', 'documents': documents},
                              output, ensure_ascii=False, indent=2)
                result['exported_documents'] = len(documents)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (SyncError, ValueError, OSError, sqlite3.Error):
        # No tracebacks: file contents, responses and env values are intentionally excluded.
        print('Projection failed. Check manifest, account permissions and pending/rate-limit ledger state. '
              'Use the recovery procedure in integrations/notion/ADAPTER.md.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
