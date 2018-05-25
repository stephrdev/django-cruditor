import os


DEBUG = True

SECRET_KEY = 'testing'

USE_TZ = True
TIME_ZONE = 'UTC'

ROOT_URLCONF = 'examples.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cruditor',
    'django_tables2',
    'django_filters',
    'tapeforms',

    'examples.store',
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'debug': True
    }
}]
