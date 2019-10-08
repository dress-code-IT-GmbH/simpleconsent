import base64
import json
import os
import requests

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


def test_verify_existing():
    entityid = 'testsp'
    entityid_b64 = base64.urlsafe_b64encode(entityid.encode('ascii'))
    consentid = '398761324012830460876'
    url = f"{origin}/has_consent/{entityid_b64.decode('ascii')}/{consentid}/"
    response = requests.request(method='GET', url=url)
    assert response.status_code == 200
    assert json.loads(response.text) == True


def test_verify_non_existing():
    entityid = 'xx'
    entityid_b64 = base64.urlsafe_b64encode(entityid.encode('ascii'))
    consentid = 'test_inv_1230982450987'
    url = f"{origin}/has_consent/{entityid_b64.decode('ascii')}/{consentid}/"
    response = requests.request(method='GET', url=url)
    assert response.status_code == 200
    assert json.loads(response.text) == False


def test_verify_revoked():
    entityid = 'https://sp1.example.com/sp'
    entityid_b64 = base64.urlsafe_b64encode(entityid.encode('ascii'))
    consentid = 'test_invalid'
    url = f"{origin}/has_consent/{entityid_b64.decode('ascii')}/{consentid}/"
    response = requests.request(method='GET', url=url)
    assert response.status_code == 200
    assert json.loads(response.text) == False
