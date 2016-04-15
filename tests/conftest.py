import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage import default_storage
from django.test.client import RequestFactory
from django.utils import translation
from django.utils.module_loading import import_string


class UserRequestFactory(RequestFactory):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', AnonymousUser())
        super(UserRequestFactory, self).__init__(*args, **kwargs)

    def request(self, *args, **kwargs):
        user = kwargs.pop('user', self.user)
        request = super(UserRequestFactory, self).request(*args, **kwargs)

        request.user = user

        request.session = import_string(settings.SESSION_ENGINE + '.SessionStore')()

        request._messages = default_storage(request)

        return request


@pytest.fixture
def user_rf(request):
    return UserRequestFactory()


@pytest.yield_fixture
def activate_en():
    original_language = translation.get_language()
    translation.activate('en')
    yield
    translation.activate(original_language)
