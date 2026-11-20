"""Lectures bornées d'une origine administrée, sous une échéance commune."""
import asyncio
from hashlib import sha256
from html.parser import HTMLParser
import json
import re
import socket
import ssl
import threading
from urllib.parse import urlsplit


class ProbeError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


class Paragraphs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_main = False
        self.current = None
        self.texts = []

    def handle_starttag(self, tag, attrs):
        # Only the deliberately plain, published diagnostic document is accepted.
        permitted = {"html": {"lang"}, "meta": {"charset"}, "title": set(),
                     "head": set(), "body": set(), "main": set(), "p": set()}
        if tag not in permitted or any(name not in permitted[tag] for name, _ in attrs):
            raise ProbeError("render")
        if tag == "main":
            self.in_main = True
        elif tag == "p" and self.in_main:
            self.current = []

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
        if tag == "p" and self.current is not None:
            self.texts.append("".join(self.current).strip())
            self.current = None


async def _connect(url, tls):
    # DNS can block beyond a socket timeout. A daemon resolver lets the CLI
    # honour its deadline even if the system resolver has not returned yet.
    loop = asyncio.get_running_loop()
    result = loop.create_future()

    def publish(addresses, error):
        if result.done():
            return
        if error:
            result.set_exception(error)
        else:
            result.set_result(addresses)

    def resolve():
        try:
            addresses = socket.getaddrinfo(url.hostname, url.port or 443, type=socket.SOCK_STREAM)
        except OSError as exc:
            answer = ([], exc)
        else:
            answer = (addresses, None)
        try:
            loop.call_soon_threadsafe(publish, *answer)
        except RuntimeError:
            pass  # The deadline expired and the event loop is closed.

    threading.Thread(target=resolve, daemon=True).start()
    addresses = await result
    last_error = OSError("Destination indisponible")
    for family, _, _, _, address in addresses:
        try:
            return await asyncio.open_connection(address[0], address[1], family=family,
                                                 ssl=tls, server_hostname=url.hostname, limit=16384)
        except ssl.SSLError:
            raise
        except OSError as exc:
            last_error = exc
    raise last_error


async def _read(url, tls, route, maximum, payload=None):
    reader, writer = await asyncio.wait_for(_connect(url, tls), timeout=2)
    try:
        method = "GET" if payload is None else "POST"
        request = f"{method} /internal/{route} HTTP/1.0\r\nHost: {url.netloc}\r\nConnection: close\r\n"
        if payload is not None:
            request += f"Content-Type: application/json\r\nContent-Length: {len(payload)}\r\n"
        writer.write((request + "\r\n").encode("ascii"))
        if payload is not None:
            writer.write(payload)
        await writer.drain()
        block = await reader.readuntil(b"\r\n\r\n")
        status_line, *lines = block[:-4].decode("latin-1").split("\r\n")
        protocol, status, *_ = status_line.split()
        if protocol not in ("HTTP/1.0", "HTTP/1.1"):
            raise ProbeError("incompatible")
        if status in ("401", "403"):
            raise ProbeError("authentication")
        if status == "404" and route.startswith(("editorial/", "preview/")):
            raise ProbeError("inaccessible")
        if route.startswith("preview/") and status == "409":
            raise ProbeError("changed")
        if status == "503":
            raise ProbeError("unavailable")
        if status != "200":
            raise ProbeError("incompatible")
        headers = {}
        for line in lines:
            name, value = line.split(":", 1)
            key = name.lower()
            if key in headers and key in ("content-type", "content-length", "x-studio-site", "x-studio-instance"):
                raise ProbeError("incompatible")
            headers[key] = value.strip()
        if "transfer-encoding" in headers or "content-encoding" in headers:
            raise ProbeError("incompatible")
        body = bytearray()
        while len(body) <= maximum:
            chunk = await reader.read(min(8192, maximum + 1 - len(body)))
            if not chunk:
                break
            body.extend(chunk)
        if len(body) > maximum or int(headers.get("content-length", len(body))) != len(body):
            raise ProbeError("incompatible")
        return headers, body.decode("utf-8")
    finally:
        writer.close()


def _versions(profile, data):
    if (type(data.get("contract_minor")) is not int or not 0 <= data["contract_minor"] <= 2147483647
            or data.get("engine_version") != profile.engine_version or data.get("image_digest") != profile.image_digest
            or not isinstance(data.get("wagtail_version"), str) or not 0 < len(data["wagtail_version"].strip()) <= 64):
        raise ProbeError("incompatible")
    versions = {k: data[k] for k in ("contract_major","contract_minor","engine_version","wagtail_version","image_digest")}
    capabilities = data.get("capabilities", [])
    if (not isinstance(capabilities, list) or len(capabilities) > 64
            or any(not isinstance(cap, str) or len(cap) > 128 for cap in capabilities)):
        raise ProbeError("incompatible")
    supported = [name for name in ("editorial.published.v1", "preview.v1") if name in capabilities]
    if supported:
        versions["capabilities"] = supported
    return versions


async def _probe(profile, tls):
    url = urlsplit(profile.origin)
    versions = {}
    for route in ("identity", "version", "health", "render"):
        html = route == "render"
        headers, body = await _read(url, tls, route, 65536 if html else 16384)
        mime = headers.get("content-type", "").split(";")[0].strip().lower()
        if mime != ("text/html" if html else "application/json"):
            raise ProbeError("incompatible")
        data = headers if html else json.loads(body)
        if not isinstance(data, dict):
            raise ProbeError("incompatible")
        identity = ("x-studio-site", "x-studio-instance") if html else ("site_id", "instance_id")
        if (data.get(identity[0]), data.get(identity[1])) != (str(profile.site_id), str(profile.instance_id)):
            raise ProbeError("identity")
        if route in ("identity","version") and (type(data.get("contract_major")) is not int or data["contract_major"] != 1):
            raise ProbeError("incompatible")
        if route == "version":
            versions = _versions(profile, data)
        elif route == "health" and data.get("status") != "ready":
            raise ProbeError("unavailable")
        elif html:
            parser = Paragraphs()
            parser.feed(body)
            parser.close()
            if parser.texts != [profile.marker]:
                raise ProbeError("render")
    return versions


def _run(profile, operation, *args):
    try:
        tls = ssl.create_default_context(cafile=profile.ca)
        tls.load_cert_chain(profile.cert, profile.key, password=lambda: "")
        return asyncio.run(asyncio.wait_for(operation(profile, tls, *args), timeout=10))
    except ssl.SSLError:
        raise ProbeError("authentication") from None
    except TimeoutError:
        raise ProbeError("timeout") from None
    except (OSError, asyncio.IncompleteReadError):
        raise ProbeError("communication") from None
    except (ValueError, UnicodeError, asyncio.LimitOverrunError, RecursionError):
        raise ProbeError("incompatible") from None


def probe(profile):
    return _run(profile, _probe)


async def _published(profile, tls, page_number):
    headers, body = await _read(urlsplit(profile.origin), tls, f"editorial/v1/article/{page_number}", 16384)
    if headers.get("content-type", "").split(";")[0].strip().lower() != "application/json":
        raise ProbeError("incompatible")
    data = json.loads(body)
    if (not isinstance(data, dict) or set(data) != {"site_id", "instance_id", "type", "page_id", "published_revision_id"}
            or data["type"] != "article" or type(data["page_id"]) is not int or data["page_id"] != page_number
            or (data["site_id"], data["instance_id"]) != (str(profile.site_id), str(profile.instance_id))
            or not isinstance(data["published_revision_id"], str)
            or not re.fullmatch(r"[1-9][0-9]{0,31}", data["published_revision_id"])):
        raise ProbeError("incompatible")
    return data["published_revision_id"]


def read_published_article(profile, page_number):
    if type(page_number) is not int or not 0 < page_number <= 2147483647:
        raise ProbeError("inaccessible")
    try:
        return _run(profile, _published, page_number)
    except ProbeError as error:
        if error.code == "inaccessible":
            raise
        raise ProbeError("indisponible") from None

def canonical_json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":")).encode("utf-8")


async def _preview(profile, tls, payload):
    # Validate this origin before transmitting a private composition.
    url = urlsplit(profile.origin)
    for route in ("identity", "version"):
        headers, body = await _read(url, tls, route, 16384)
        if headers.get("content-type", "").partition(";")[0].strip().lower() != "application/json":
            raise ProbeError("incompatible")
        data = json.loads(body)
        if (not isinstance(data, dict) or data.get("site_id") != str(profile.site_id)
                or data.get("instance_id") != str(profile.instance_id)):
            raise ProbeError("identity")
        if type(data.get("contract_major")) is not int or data["contract_major"] != 1:
            raise ProbeError("incompatible")
    versions = _versions(profile, data)
    if "preview.v1" not in versions.get("capabilities", []):
        raise ProbeError("incompatible")
    digest = sha256(canonical_json(payload)).hexdigest()
    request = canonical_json({"payload": payload, "sha256": digest})
    if len(request) > 4 * 1024 * 1024:
        raise ProbeError("incompatible")
    headers, body = await _read(url, tls, "preview/v1/render", 8 * 1024 * 1024, request)
    if headers.get("content-type", "").partition(";")[0].strip().lower() != "application/json":
        raise ProbeError("incompatible")
    result = json.loads(body)
    if (not isinstance(result, dict) or not isinstance(result.get("manifest"), dict)
            or result["manifest"].get("wagtail_version") != versions["wagtail_version"]):
        raise ProbeError("incompatible")
    return result


def read_preview(profile, payload):
    return _run(profile, _preview, payload)
