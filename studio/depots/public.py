from functools import wraps
from uuid import UUID, uuid4

from django.conf import settings
from django.core import signing
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.cache import add_never_cache_headers
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods, require_safe

from registre.services import Conflict

from . import services


CAPABILITY_COOKIE = "depot_acces"
PORTAL_PATH = "/depot/"


def private_response(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        response = view(request, *args, **kwargs)
        add_never_cache_headers(response)
        response["Referrer-Policy"] = "same-origin"
        response["X-Content-Type-Options"] = "nosniff"
        response["Content-Security-Policy"] = (
            "default-src 'none'; style-src 'self'; script-src 'self'; font-src 'self'; "
            "form-action 'self'; frame-ancestors 'none'; base-uri 'none'"
        )
        return response
    return wrapped


def see_other(name, *args):
    return HttpResponse(status=303, headers={"Location": reverse(f"depot_public:{name}", args=args)})


def page(request, screen, *, status=200, **context):
    return render(request, "depots/public.html", {
        "screen": screen, "contact": settings.STUDIO_PORTAL_CONTACT, **context,
    }, status=status)


def unavailable(request):
    response = page(request, "unavailable", status=404)
    response.delete_cookie(CAPABILITY_COOKIE, path=PORTAL_PATH, samesite="Strict")
    return response


def limit_response(request, error, **context):
    screen = "form" if context else "limited"
    response = page(request, screen, status=429, limit=True, retry_after=error.retry_after, **context)
    if error.retry_after is not None:
        response["Retry-After"] = str(error.retry_after)
    return response


@private_response
@require_http_methods(["GET", "HEAD", "POST"])
@sensitive_post_parameters()
def entry(request):
    if request.method != "POST":
        return page(request, "entry")
    try:
        capability, expires_at = services.exchange(request.POST.get("code", ""), request.META.get("REMOTE_ADDR", ""))
    except services.InvalidInvitation:
        return unavailable(request)
    except services.RateLimited as error:
        response = limit_response(request, error)
        response.delete_cookie(CAPABILITY_COOKIE, path=PORTAL_PATH, samesite="Strict")
        return response
    response = see_other("deposit")
    response.set_cookie(
        CAPABILITY_COOKIE, capability, max_age=max(1, int((expires_at - timezone.now()).total_seconds())),
        path=PORTAL_PATH, httponly=True, secure=settings.STUDIO_PORTAL_ORIGIN.startswith("https://"),
        samesite="Strict",
    )
    return response


@private_response
@require_http_methods(["GET", "HEAD", "POST"])
@sensitive_post_parameters()
def deposit(request):
    capability = request.COOKIES.get(CAPABILITY_COOKIE, "")
    try:
        invitation = services.invitation_for(capability)
    except services.InvalidInvitation:
        return unavailable(request)
    # A form left open in another tab must not submit into a different invitation.
    signer = signing.Signer(salt=f"depots.submission.{invitation.pk}")
    if request.method != "POST":
        return page(request, "form", invitation=invitation, request_id=signer.sign(str(uuid4())))
    request_id = request.POST.get("request_id", "")
    try:
        repeat_key = UUID(signer.unsign(request_id))
    except (ValueError, signing.BadSignature):
        return page(request, "conflict", status=409)
    figma_url = request.POST.get("figma_url", "")
    comment = request.POST.get("comment", "")
    context = dict(invitation=invitation, request_id=request_id, figma_url=figma_url, comment=comment)
    try:
        result = services.submit(capability, repeat_key, figma_url, comment)
    except services.InvalidInvitation:
        return unavailable(request)
    except ValidationError as error:
        return page(request, "form", status=422, errors=error.message_dict, **context)
    except services.RateLimited as error:
        return limit_response(request, error, **context)
    except Conflict:
        return page(request, "conflict", status=409)
    return see_other("receipt", result.pk)


@private_response
@require_safe
def receipt(request, submission_id):
    try:
        result = services.receipt(request.COOKIES.get(CAPABILITY_COOKIE, ""), submission_id)
    except services.InvalidInvitation:
        return unavailable(request)
    except Http404:
        return page(request, "missing_receipt", status=404)
    return page(request, "receipt", submission=result)
