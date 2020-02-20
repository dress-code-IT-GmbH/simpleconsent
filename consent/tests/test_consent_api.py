import base64
import json
import requests
from consent.models import Consent
import pytest
from django.core.management import call_command
from pathlib import Path

consent_data = Path('consent/tests/fixtures/testset1.json')



apicred = ('admin', 'adminadmin')


@pytest.mark.django_db()
def test_verify_existing(live_server):
    entityid = 'testsp'
    entityid_b64 = base64.urlsafe_b64encode(entityid.encode('ascii'))
    consentid = '398761324012830460876'
    url = f"{live_server}/has_consent/{entityid_b64.decode('ascii')}/{consentid}/"
    response = requests.request(method='GET', url=url)
    assert response.status_code == 401
    response = requests.request(method='GET', url=url, auth=apicred)
    assert response.status_code == 200
    assert json.loads(response.text) is True


@pytest.mark.django_db()
def not_test_verify_existing_second(live_server):
    entityid = 'testsp'
    entityid_b64 = base64.urlsafe_b64encode(entityid.encode('ascii'))
    consentid = '398761324012830460876'
    url = f"{live_server}/has_consent/{entityid_b64.decode('ascii')}/{consentid}/"
    response = requests.request(method='GET', url=url)
    assert response.status_code == 401
    response = requests.request(method='GET', url=url, auth=apicred)
    assert response.status_code == 200
    assert json.loads(response.text) is True


def test_verify_non_existing(live_server):
    entityid = 'xx'
    entityid_b64 = base64.urlsafe_b64encode(entityid.encode('ascii'))
    consentid = 'test_inv_1230982450987'
    url = f"{live_server}/has_consent/{entityid_b64.decode('ascii')}/{consentid}/"
    response = requests.request(method='GET', url=url, auth=apicred)
    assert response.status_code == 200
    assert json.loads(response.text) is False


def test_verify_revoked(live_server):
    entityid = 'https://sp1.example.com/sp'
    entityid_b64 = base64.urlsafe_b64encode(entityid.encode('ascii'))
    consentid = 'test_invalid'
    url = f"{live_server}/has_consent/{entityid_b64.decode('ascii')}/{consentid}/"
    response = requests.request(method='GET', url=url, auth=apicred)
    assert response.status_code == 200
    assert json.loads(response.text) is False
