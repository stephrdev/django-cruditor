import pytest
from django.contrib.auth.models import User

from cruditor.filters import AnyChoiceFilter, MultiFieldFilter

from .factories import UserFactory


class TestAnyChoiceFilter:

    def test_anychoicefilter_init(self, activate_en):
        instance = AnyChoiceFilter(choices=(('foo', 'FOO'), ('bar', 'BAR')))
        assert len(instance.extra['choices']) == 3
        assert instance.extra['choices'][0] == ('', 'Any choice')

    def test_anychoicefilter_custom_empty_label(self, activate_en):
        instance = AnyChoiceFilter(
            empty_label='Lorem', choices=(('foo', 'FOO'), ('bar', 'BAR')))
        assert len(instance.extra['choices']) == 3
        assert instance.extra['choices'][0] == ('', 'Lorem')


@pytest.mark.django_db
class TestMultiFieldFilter:

    def setup(self):
        self.users = UserFactory.create_batch(3)

    def test_init(self):
        instance = MultiFieldFilter(['username'])
        assert instance.fields == ['username']

    def test_filter_no_fields(self):
        instance = MultiFieldFilter([])
        user_qs = User.objects.all()
        assert instance.filter(user_qs, 'Foo') == user_qs

    def test_filter_no_value(self):
        instance = MultiFieldFilter(['username'])
        user_qs = User.objects.all()
        assert instance.filter(user_qs, '') == user_qs

    def test_filter(self):
        instance = MultiFieldFilter(['username', '=first_name'])
        assert instance.filter(
            User.objects.all(), self.users[0].username).get() == self.users[0]
        assert instance.filter(
            User.objects.all(), self.users[1].first_name).get() == self.users[1]
