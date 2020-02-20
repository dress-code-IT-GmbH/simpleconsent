import pytest
from pathlib import Path
from django.core.management import call_command
import os
from pytest_django.fixtures import transactional_db as orig_transactional_db


consent_data = Path('consent/tests/fixtures/testset1.json')


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', consent_data)


