import base64
import json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.template import loader
from consent.models import Consent


def has_consent(request: HttpRequest, entityid_b64: str, consentid: str) -> HttpResponse:
    """ Test if a consent exists for a given active entityID/consentid pair """
    entityid_bytes = base64.urlsafe_b64decode(entityid_b64.encode('ascii'))
    try:
        _consent = Consent.objects.get(entityID=entityid_bytes.decode('ascii'), consentid=consentid, revoked_at=None)
        return HttpResponse('true', status=200)
    except ObjectDoesNotExist:
        return HttpResponse('false', status=200)


def display_consent_request(request: HttpRequest, consent_requ_json_b64: str) -> HttpResponse:
    consent_request_json = base64.urlsafe_b64decode(consent_requ_json_b64.encode('ascii'))
    consent_request = json.loads(consent_request_json)
    consent_request ['consent_requ_json_b64'] = consent_requ_json_b64  # required for submit link
    template = loader.get_template('consent/index.html')
    contents = template.render(consent_request, request)
    return HttpResponse(contents)


def accept_consent(request: HttpRequest, consent_requ_json_b64: str) -> HttpResponse:
    consent_request_json = base64.urlsafe_b64decode(consent_requ_json_b64.encode('ascii'))
    consent_request = json.loads(consent_request_json)

    if len(Consent.objects.filter(entityID=consent_request['entityid'], consentid=consent_request['consentid'], revoked_at=None)) == 0:
        consent = Consent()
        consent.entityID = consent_request['entityid']
        consent.consentid = consent_request['consentid']
        consent.sp_displayname = consent_request['sp']
        consent.consent_text = ', '.join(consent_request['attr_list'])
        consent.save()

    return HttpResponseRedirect(settings.REDIRECT_AFTER_CONSENT)


def decline_consent(request: HttpRequest) -> HttpResponse:
    return HttpResponseRedirect(settings.REDIRECT_AFTER_CONSENT)
