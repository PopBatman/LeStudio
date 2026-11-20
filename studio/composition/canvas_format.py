from django.http import Http404


FORMATS = {"base": ("Bureau", 1200), "tablet": ("Tablette", 820), "mobile": ("Mobile", 390)}


def canvas_format(params):
    fmt = params.get("format", "base")
    if fmt not in FORMATS:
        raise Http404
    if params.get("largeur"):
        try:
            width = int(params["largeur"])
        except (TypeError, ValueError):
            raise Http404 from None
        if not 320 <= width <= 1920:
            raise Http404
        return ("mobile" if width < 768 else "tablet" if width < 1024 else "base"), width
    return fmt, FORMATS[fmt][1]
