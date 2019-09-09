from simpleconsent.settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# overwrite default database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
