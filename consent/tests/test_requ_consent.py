import base64
import json
import os
import requests
import hashlib
import hmac
from pathlib import Path

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simpleconsent.settings_unittest")
django.setup()
from django.conf import settings


CONSENTID = 'test_inv_2'
CONSENT_REQUEST = {
    'entityid': 'xx',
    'consentid': CONSENTID,
    "displayname": 'Franz Xaver Muster',
    "mail": 'fxmuster',
    'sp': 'TEST SP1',
    'attr_list': ['first_name', 'last_name', 'email'],
}


# call this test twice: once default, and another time when simeplconsent has been started with CONSENT_TEMPLATE set
def test_display_consent_request(live_server):
    consent_request_json = json.dumps(CONSENT_REQUEST)
    hmac_str = hmac.new(settings.PROXY_HMAC_KEY, consent_request_json.encode('utf-8'), hashlib.sha256).hexdigest()
    consent_request_json_b64 = base64.urlsafe_b64encode(consent_request_json.encode('ascii'))
    url = f"{live_server}/request_consent/{consent_request_json_b64.decode('ascii')}/{hmac_str}/"
    response = requests.request(method='GET', url=url)
    assert response.status_code == 200
    Path('consent/tests/testout/display_consent.html').write_text(response.content.decode('utf-8'))
    if os.getenv('CONSENT_TEMPLATE', '') == 'example/templates/index.html':
        assert Path('consent/tests/expected_results/display_consent_custom.html').read_text() == response.content.decode('utf-8')
    else:
        assert Path('consent/tests/expected_results/display_consent_default.html').read_text() == response.content.decode('utf-8')


# def test_accept_consent_request():
#     q = Consent.objects.filter(consentid=CONSENTID)
#     if q:
#         q[0].delete()
#     consent_request_json = json.dumps(CONSENT_REQUEST)
#     hmac_str = hmac.new(settings.PROXY_HMAC_KEY, consent_request_json.encode('utf-8'), hashlib.sha256).hexdigest()
#     consent_request_json_b64 = base64.urlsafe_b64encode(consent_request_json.encode('ascii'))
#     url = f"{origin}/accept_consent/{consent_request_json_b64.decode('ascii')}/{hmac_str}/"
#     response = requests.request(method='GET', url=url, allow_redirects=False)
#     assert response.status_code == 302
#     # following test does not work because the unit test has a different DB instance than the web app
#     # need to believe in manual testing here
#     # q = Consent.objects.filter(consentid=CONSENTID)
#     # assert len(q) == 1
#     url = f"{origin}/accept_consent/{consent_request_json_b64.decode('ascii')}/{'x' + hmac_str[1:]}/"
#     response = requests.request(method='GET', url=url)
#     assert response.status_code == 500
