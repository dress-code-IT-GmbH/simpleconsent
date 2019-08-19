import os
from pathlib import Path

import coreapi
import django
import django.core.files
import pytest
from django.conf import settings

from PVZDpy.tests.common_fixtures import ed_path
from common.show_env import show_env
from consent.constants import STATUSGROUP_FRONTEND
from consent.models.consent import consent
assert 'portaladmin' in settings.INSTALLED_APPS

pytestmark = pytest.mark.django_db
django.setup()


path_expected_results = 'expected_results'

def assert_equal(expected, actual, fn=''):
    # workaround because pycharm does not display the full string (despite pytest -vv etc)
    msg = fn+"\n'"+actual+"' != '"+expected+"' "
    assert expected == actual, msg


def fixture_testdata_basedir():
    return Path(settings.BASE_DIR) / 'PVZDlib' / 'PVZDpy' / 'tests' / 'testdata' / 'saml'


def fixture_result(filename):
    p = Path(settings.BASE_DIR) / 'portaladmin' / 'tests' / path_expected_results / filename
    with p.open() as fd:
        return fd.read()


@pytest.mark.show_testenv
def test_show_env(capfd):
    with capfd.disabled():
        show_env(__name__)


@pytest.mark.requires_webapp
def test_api_update_ed_signed():
    ''' update ed_signed via API
        requires PVZDweb runnning on dev database (no fixture yet for this)
    '''
    fn = Path(ed_path(22, dir=fixture_testdata_basedir()))
    with fn.open('rb') as fd:
        django_file = django.core.files.File(fd)
        mds = consent()
        count = consent.objects.filter(entityID='https://idp22.identinetics.com/idp.xml', statusgroup=STATUSGROUP_FRONTEND)
        if count:
            mds = consent.objects.get(entityID='https://idp22.identinetics.com/idp.xml', statusgroup=STATUSGROUP_FRONTEND)
            mds.ed_signed = ''
            mds.save()
        else:
            django_file = django.core.files.File(fd)
            mds = consent()
            mds.ed_file_upload.save(fn.name, django_file, save=True)
        update_id = mds.id

    client = coreapi.Client()
    schema = client.get("http://localhost:8000/docs/")

    action = ["mdstatement", "partial_update"]
    params = {
        "id": update_id,
        "admin_note": "Updated ed_signed from REST API",
        "ed_signed": fn.read_text(),
    }
    result = client.action(schema, action, params=params)
    #expected_result = fixture_result('insert22.json')
    #assert_equal(expected_result, consent.objects.all()[0].serialize_json())

