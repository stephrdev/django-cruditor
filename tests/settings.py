SECRET_KEY = 'testing'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'cruditor',
]

# We really don't rely on the urlconf but we need to set a path anyway.
ROOT_URLCONF = 'django.contrib.staticfiles.urls'

STATIC_URL = '/static/'
