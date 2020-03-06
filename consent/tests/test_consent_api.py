from django.test import TestCase
import base64
import json
from django.test import Client


class ConsentCleanintTestCase(TestCase):
    fixtures = ['consent/tests/fixtures/testset1.json']

    @staticmethod
    def _basic_auth_headers():
        headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'admin:adminadmin').decode("ascii")
        }
        return headers

    @staticmethod
    def _consent_url(entityid, consentid):
        entityid_b64 = base64.urlsafe_b64encode(entityid.encode('ascii'))
        url = f"/has_consent/{entityid_b64.decode('ascii')}/{consentid}/"
        return url

    def test_verify_existing(self):
        c = Client()

        entityid = 'testsp'
        consentid = '398761324012830460876'

        url = self._consent_url(entityid, consentid)
        response = c.get(path=url)
        self.assertEqual(response.status_code, 401)

        headers = self._basic_auth_headers()
        response = c.get(path=url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), True)

    def test_verify_non_existing(self):
        c = Client()

        entityid = 'xx'
        consentid = 'test_inv_1230982450987'
        url = self._consent_url(entityid, consentid)

        headers = self._basic_auth_headers()

        response = c.get(path=url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), False)

    def test_verify_revoked(self):
        c = Client()

        entityid = 'https://sp1.example.com/sp'
        consentid = 'test_invalid'
        url = self._consent_url(entityid, consentid)

        headers = self._basic_auth_headers()

        response = c.get(path=url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), False)
