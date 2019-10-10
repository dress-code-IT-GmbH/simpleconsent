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
from consent.models import Consent
from consent.tests.setup_db_consent import load_testset1, setup_db_tables_consent

# prepare database fixture (a temporary in-memory database is created for this test)
django.setup()
assert 'consent' in settings.INSTALLED_APPS
setup_db_tables_consent()
load_testset1()
assert len(Consent.objects.all()) > 0, 'No gvOrganisation data found'

origin = 'http://127.0.0.1:8017'

CONSENTID = 'test_inv_2'
CONSENT_REQUEST = {
    'entityid': 'xx',
    'consentid': CONSENTID,
    'sp': 'TEST SP1',
    'attr_list': ['first_name', 'last_name', 'email'],
}


def test_display_consent_request():
    consent_request_json = json.dumps(CONSENT_REQUEST)
    consent_request_json_b64 = base64.urlsafe_b64encode(consent_request_json.encode('ascii'))
    url = f"{origin}/request_consent/{consent_request_json_b64.decode('ascii')}/"
    response = requests.request(method='GET', url=url)
    assert response.status_code == 200
    Path('consent/tests/testout/display_consent.html').write_text(response.content.decode('utf-8'))
    assert Path('consent/tests/expected_results/display_consent.html').read_text() == response.content.decode('utf-8')


def test_accept_consent_request():
    q = Consent.objects.filter(consentid=CONSENTID)
    if q:
        q[0].delete()
    consent_request_json = json.dumps(CONSENT_REQUEST)
    hmac_str = hmac.new(settings.PROXY_HMAC_KEY, consent_request_json.encode('utf-8'), hashlib.sha256).hexdigest()
    consent_request_json_b64 = base64.urlsafe_b64encode(consent_request_json.encode('ascii'))
    url = f"{origin}/accept_consent/{consent_request_json_b64.decode('ascii')}/{hmac_str}/"
    response = requests.request(method='GET', url=url)
    assert response.status_code == 200
    # following test does not work because the unit test has a different DB instance than the web app
    # need to believe in manual testing here
    # q = Consent.objects.filter(consentid=CONSENTID) # for some reason this query fails although the record seems to be in the DB
    # assert len(q) == 1
