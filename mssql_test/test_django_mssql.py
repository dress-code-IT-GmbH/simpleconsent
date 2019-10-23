import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simpleconsent.settings_mssql")
django.setup()
from django.conf import settings
#from django.db import connection
from consent.models import Consent
from consent.tests.setup_db_consent import load_testset1, setup_db_tables_consent

def test_connectdb():
    # prepare database fixture (a temporary in-memory database is created for this test)
    assert 'consent' in settings.INSTALLED_APPS
    setup_db_tables_consent()
    load_testset1()
    assert len(Consent.objects.all()) > 0, 'No gvOrganisation data found'


#def test_list_basetables():
#    qry = "SELECT table_name FROM information_schema.tables WHERE table_type = 'base table';"
#    cursor = connection.cursor()
#    cursor.execute(qry)
#    t = cursor.fetchall()
#    print(', '.join(t))
#    cursor.close()