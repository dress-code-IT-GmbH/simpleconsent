from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from consent.models import Consent

def has_consent(request: HttpRequest, entityid: str, userid: str) -> HttpResponse:
    consent = get_object_or_404(Consent, entityID=entityid, userid=userid, revoked_at=None)
    return HttpResponse(status=200)