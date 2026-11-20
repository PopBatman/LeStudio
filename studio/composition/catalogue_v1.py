"""Manifestes livrés avec les rendus V1. Garder ce contrat pour les anciennes révisions."""

from copy import deepcopy


TITLES = {"heading": "Titre", "text": "Texte", "container": "Conteneur",
          "image": "Image", "button": "Bouton"}
PARAMETERS = {
    "heading": {"text": "text", "level": "level"},
    "text": {"text": "text"},
    "container": {"layout": "layout"},
    "image": {"media": "media", "alt": "alt"},
    "button": {"label": "label", "url": "https"},
    "article": {"content": "wagtail_content"},
    "signature": {"text": "text"},
}


def manifest(renderer):
    return {
        "props": deepcopy(PARAMETERS[renderer]),
        "variants": ["primary", "secondary"] if renderer == "button" else ["default"],
        "tokens": ["accent", "background", "ink", "font", "gap"],
    }
