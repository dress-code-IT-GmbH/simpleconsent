import os
from pathlib import Path

import django
import pytest
from django.conf import settings

from PVZDpy.tests.common_fixtures import ed_path
from common.recreate_db import recreate_db
from common.show_env import show_env
from fedop.models.policystorage import PolicyStorage
from fedop.tests.setup_db_fedop import loaddata_fedop1, setup_db_tables_fedop
from consent.models.consent import consent
from consent.tests.setup_db_portaladmin import setup_db_tables_portaladmin
from tnadmin.models.gvorg import GvOrganisation
from tnadmin.tests.setup_db_tnadmin import load_tnadmin1, setup_db_tables_tnadmin

# prepare database fixture (a temporary in-memory database is created for this test)
pytestmark = pytest.mark.unittest_db
assert 'portaladmin' in settings.INSTALLED_APPS
django.setup()
recreate_db() # drop/create db before django opens a connection
setup_db_tables_tnadmin()
setup_db_tables_fedop()
setup_db_tables_portaladmin()
load_tnadmin1()
loaddata_fedop1()
assert len(GvOrganisation.objects.all()) > 0, 'No gvOrganisation data found'

path_expected_results = 'expected_results'
path_testout = Path('portaladmin/tests/testout')
path_testout.mkdir(parents=True)


def test_policy_journal():
    assert 1 == len(PolicyStorage.objects.all()), 'PolicyStorage is a singleton, number or records must be equal 1'

def assert_equal(expected, actual, fn='', ed_path_no: int=None):
    # workaround because pycharm does not display the full string (despite pytest -vv etc)
    msg = fn+"\n'"+actual+"' != '"+expected+"' "
    p_testout = Path(path_testout / f"insert{ed_path_no}.json").resolve()
    with p_testout.open('w') as fd:
        fd.write(actual)
    assert expected == actual, msg


def fixture_testdata_basedir():
    return Path(settings.BASE_DIR) / 'PVZDlib' / 'PVZDpy' / 'tests' / 'testdata' / 'saml'


def fixture_result(filename):
    p = Path(settings.BASE_DIR) / 'portaladmin' / 'tests' / path_expected_results / filename
    with p.open() as fd:
        return fd.read()

@pytest.fixture
def config_file() -> None:
    os.environ['PVZDLIB_CONFIG_MODULE'] = str(Path(settings.BASE_DIR)  / 'fedop/config/pvzdlib_config.py')


@pytest.mark.show_testenv
def test_show_env(capfd):
    with capfd.disabled():
        show_env(__name__)


@pytest.mark.parametrize('expected_result_fn, ed_path_no', [
                          ('insert01.json', 1),
                          ('insert02.json', 2),
                          ('insert03.json', 3),
                          ('insert04.json', 4),
                          ('insert05.json', 5),
                          ('insert06.json', 6),
                          ('insert07.json', 7),
                          ('insert08.json', 8),
                          ('insert09.json', 9),
                          ('insert10.json', 10),
                          ('insert11.json', 11),
                          ('insert12.json', 12),
                          ('insert13.json', 13),
                          ('insert14.json', 14),
                          ('insert15.json', 15),
                          # ('insert16.json', 16),   # causes unique constraint violation
                          # ('insert17.json', 17),   # causes unique constraint violation
                          ('insert18.json', 18),
                          #('insert19.json', 19),    # causes unique constraint violation
                          # ('insert20.json', 20),   # causes unique constraint violation
                          ('insert21.json', 21),
                          ('insert22.json', 22),
                          ('insert23.json', 23),
                          ])
def test_insert_and_update(config_file, expected_result_fn, ed_path_no):
    fn = Path(ed_path(ed_path_no, dir=fixture_testdata_basedir()))
    with fn.open('rb') as fd:
        django_file = django.core.files.File(fd)
        mds = consent()
        mds.ed_file_upload.save(fn.name, django_file, save=True)
    expected_result = fixture_result(expected_result_fn)
    assert_equal(expected_result, consent.objects.all()[0].serialize_json(), ed_path_no=ed_path_no)
    if ed_path_no < 4:
        mds = consent.objects.get(id=ed_path_no)
        mds.admin_note = f"some text fromt test {ed_path_no}"
        mds.save()
        mds = consent.objects.get(id=ed_path_no)
        assert mds.admin_note == f"some text fromt test {ed_path_no}"

#def test_unique_constraint() # TODO

