"""Profils d'exploitation montés en lecture seule par l'administrateur."""
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
from urllib.parse import urlsplit
from uuid import UUID


class ProfileError(Exception):
    pass


@dataclass(frozen=True)
class Profile:
    alias: str
    site_id: UUID
    instance_id: UUID
    origin: str
    ca: str
    cert: str
    key: str
    engine_version: str
    image_digest: str
    marker: str
    admin_url: str = ""


def load_profile(alias):
    try:
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", alias):
            raise ValueError
        with Path(os.environ["STUDIO_ENGINE_PROFILES"]).open("rb") as file:
            raw = file.read(262145)
        if len(raw) > 262144:
            raise ValueError
        item = json.loads(raw)[alias]
        profile = Profile(alias=alias, **{**item, "site_id": UUID(item["site_id"]),
                                          "instance_id": UUID(item["instance_id"])})
        url = urlsplit(profile.origin)
        if (url.scheme != "https" or not url.hostname or url.username is not None
                or url.password is not None or url.path not in ("", "/") or url.query or url.fragment
                or not re.fullmatch(r"[A-Za-z0-9.:-]+|\[[0-9a-fA-F:]+\](?::[0-9]+)?", url.netloc)
                or url.port == 0):
            raise ValueError
        if not all(isinstance(value, str) and value.startswith("/") for value in (profile.ca, profile.cert, profile.key)):
            raise ValueError
        if not re.fullmatch(r"sha256:[a-f0-9]{64}", profile.image_digest):
            raise ValueError
        for value in (profile.engine_version, profile.marker):
            if not isinstance(value, str) or not value.strip() or len(value) > 512:
                raise ValueError
        if profile.admin_url != "" and not valid_admin_url(profile.admin_url):
            raise ValueError
        return profile
    except (OSError, ValueError, TypeError, KeyError, AttributeError, RecursionError):
        raise ProfileError("Profil de raccordement indisponible ou invalide.") from None


def valid_admin_url(value):
    if not isinstance(value, str) or len(value) > 512 or not re.fullmatch(r"[!-~]+", value):
        return False
    url = urlsplit(value)
    if (not url.hostname or url.username is not None or url.password is not None
            or url.path != "/admin/" or url.query or url.fragment or url.port == 0
            or not re.fullmatch(r"[A-Za-z0-9.:-]+|\[[0-9a-fA-F:]+\](?::[0-9]+)?", url.netloc)):
        return False
    return url.scheme == "https" or (
        url.scheme == "http" and url.hostname in ("localhost", "127.0.0.1", "::1"))
