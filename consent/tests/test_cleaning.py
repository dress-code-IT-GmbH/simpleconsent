from django.test import TestCase
from consent.models import Consent
import random
import string
from django.db import models


class ConsentCleanintTestCase(TestCase):
    def __init__(self, method_name):
        self.long_displayname = self._create_long_string(Consent.SP_DISPLAYNAME_LENGTH + 1)
        self.shortened_displayname = self.long_displayname[:Consent.SP_DISPLAYNAME_LENGTH]
        super().__init__(method_name)

    @staticmethod
    def _create_long_string(length):
        x = ''.join(random.choice(string.ascii_letters) for _ in range(length))
        return x

    def test_save(self):
        uid = self._create_long_string(2048)
        realuid = uid[:Consent.UID_MAX_LENGTH]
        consent = Consent(
            uid=uid,
            displayname=self._create_long_string(2048),
            consentid=self._create_long_string(2048),
            entityID=self._create_long_string(2048),
            sp_displayname=self._create_long_string(2048),
        )
        consent.save()
        saved_consent = Consent.objects.get(uid=realuid)
        for f in saved_consent._meta.fields:
            if isinstance(f, models.CharField):
                value = "{}:{}".format(f.attname, getattr(saved_consent, f.attname))
                value_short = "{}:{}".format(f.attname, getattr(saved_consent, f.attname)[:f.max_length])
                self.assertEqual(value_short, value)
        return None
