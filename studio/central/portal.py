"""Origin of the invitation links and route boundary for a dedicated public host."""
import re
from urllib.parse import urlsplit

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseNotFound


def portal_origin(value):
    try:
        address = urlsplit(value)
        host = address.hostname
        port = address.port
        if (not host or host.endswith(".") or not re.fullmatch(r"[a-zA-Z0-9.-]+", host)
                or address.netloc.lower() != host + (f":{port}" if port else "")
                or address.path not in ("", "/") or address.query or address.fragment
                or address.scheme not in ("http", "https")
                or (address.scheme == "http" and host not in ("localhost", "127.0.0.1"))):
            raise ValueError
    except ValueError:
        raise ImproperlyConfigured("STUDIO_PORTAL_ORIGIN doit désigner une origine HTTPS ou la boucle locale HTTP.") from None
    return f"{address.scheme}://{address.netloc.lower()}"


PUBLIC_ASSETS = {"/assets/depot-public.js", "/assets/depot-public.css", "/assets/fonts/dm-sans-latin.woff2"}


class PortalHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_host = settings.STUDIO_PORTAL_PUBLIC_HOST
        if public_host and urlsplit("//" + request.get_host()).hostname.rstrip(".") == public_host:
            if not request.path_info.startswith("/depot/") and request.path_info not in PUBLIC_ASSETS:
                return HttpResponseNotFound()
        return self.get_response(request)
