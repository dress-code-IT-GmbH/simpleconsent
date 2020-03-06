from django.test import TestCase
from django.test import Client
from pathlib import Path
import base64
import json
import os
import hashlib
import hmac
from . import my_django_setup
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


class DisplayConsentTestCase(TestCase):
    fixtures = ['consent/tests/fixtures/testset1.json']

    def test_display_consent_request(self):
        consent_request_json = json.dumps(CONSENT_REQUEST)
        hmac_str = hmac.new(settings.PROXY_HMAC_KEY, consent_request_json.encode('utf-8'), hashlib.sha256).hexdigest()
        consent_request_json_b64 = base64.urlsafe_b64encode(consent_request_json.encode('ascii'))
        url = f"/request_consent/{consent_request_json_b64.decode('ascii')}/{hmac_str}/"

        c = Client()
        response = c.get(path=url)
        self.assertEqual(response.status_code, 200)

        Path('consent/tests/testout/display_consent.html').write_text(response.content.decode('utf-8'))
        if os.getenv('CONSENT_TEMPLATE', '') == 'example/templates/index.html':
            self.assertEqual(
                Path('consent/tests/expected_results/display_consent_custom.html').read_text(),
                response.content.decode('utf-8')
            )
        else:
            self.assertEqual(
                Path('consent/tests/expected_results/display_consent_default.html').read_text(),
                response.content.decode('utf-8')
            )
