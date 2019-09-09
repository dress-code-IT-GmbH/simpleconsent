import base64
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.template import loader
from consent.models import Consent


def has_consent(request: HttpRequest, entityid_b64: str, userid: str) -> HttpResponse:
    """ Test if a consent exists for a given entityID/userid pair and return HTTP status 200 or 404 """
    entityid_bytes = base64.urlsafe_b64decode(entityid_b64.encode('ascii'))
    _consent = get_object_or_404(Consent, entityID=entityid_bytes.decode('ascii'), userid=userid, revoked_at=None)
    return HttpResponse(status=200)


def display_consent_request(request: HttpRequest, consent_requ_json_b64: str) -> HttpResponse:
    consent_request_json = base64.urlsafe_b64decode(consent_requ_json_b64.encode('ascii'))
    consent_request = json.loads(consent_request_json)
    consent_request = {
        'entityid': 'xx',
        'userid': 'test_inv_2',
        'sp': 'TEST SP1',
        'attr_list': ['first_name', 'last_name', 'email'],
        'consent_requ_json_b64': consent_requ_json_b64,
    }
    template = loader.get_template('consent/index.html')
    contents = template.render(consent_request, request)
    return HttpResponse(contents)

def accept_consent(request: HttpRequest, consent_requ_json_b64: str) -> HttpResponse:
    consent = Consent()
    consent.entityid = 'xx'
    consent.userid = 'test_inv_3'
    consent.sp_displayname = 'TEst SP2'
    consent.consent_text = ', '.join(['first_name', 'last_name', 'email'])
    consent.save()

    return HttpResponseRedirect('/admin')