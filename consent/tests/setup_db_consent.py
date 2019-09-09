from pathlib import Path
from django.core import management

# pytestmark = pytest.mark.django_db  # not working for whatever reason.
                                      # workaround from https://github.com/pytest-dev/pytest-django/issues/396
from pytest_django.plugin import _blocking_manager
from django.db.backends.base.base import BaseDatabaseWrapper
_blocking_manager.unblock()
_blocking_manager._blocking_wrapper = BaseDatabaseWrapper.ensure_connection


def setup_db_tables_consent():
    with open('/tmp/consent_testout_migratedb.log', 'w') as fd:
        management.call_command('migrate', '', stdout=fd)


def load_testset1():
    consent_data = Path('consent/tests/fixtures/testset1.json')
    assert consent_data.is_file(), f'could not find file {consent_data}'
    management.call_command('loaddata', consent_data)
