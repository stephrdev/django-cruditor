import django_filters
import pytest
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms.models import inlineformset_factory

from cruditor.views import (
    Cruditor403View, Cruditor404View, CruditorAddView, CruditorChangePasswordView,
    CruditorChangeView, CruditorDeleteView, CruditorListView, CruditorLogoutView)

from .factories import UserFactory


class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ('is_staff',)


@pytest.mark.django_db
class TestListView:

    def setup(self):
        self.view = CruditorListView.as_view(model=User)
        self.filtered_view = CruditorListView.as_view(
            model=User, filter_class=UserFilter)

        self.user = UserFactory.create(is_staff=False)
        self.staff_user = UserFactory.create(is_staff=True)

    def test_not_logged_in(self, user_rf):
        response = self.view(user_rf.get('/'))
        assert response.status_code == 200
        assert response.template_name == 'cruditor/login.html'
        assert 'table' not in response.context_data

    def test_logged_in_no_staff(self, user_rf):
        response = self.view(user_rf.get('/', user=self.user))
        assert response.status_code == 200
        assert response.template_name == 'cruditor/login.html'
        assert 'table' not in response.context_data

    def test_logged_in_no_permission(self, user_rf):
        view = CruditorListView.as_view(
            model=User, required_permission='accounts.change_user')

        with pytest.raises(PermissionDenied):
            view(user_rf.get('/', user=self.staff_user))

    def test_logged_in_has_permission(self, user_rf):
        self.staff_user.is_superuser = True
        view = CruditorListView.as_view(
            model=User, required_permission='accounts.change_user')

        assert view(user_rf.get('/', user=self.staff_user)).status_code == 200

    def test_get(self, user_rf):
        response = self.view(user_rf.get('/', user=self.staff_user))
        assert response.status_code == 200
        assert response.template_name == ['cruditor/list.html']
        assert response.context_data['filter_form'] is None

        table_data = list(response.context_data['table'].data.queryset.order_by('pk'))
        assert table_data == list(User.objects.all().order_by('pk'))

    def test_filter(self, user_rf):
        response = self.filtered_view(user_rf.get('/', user=self.staff_user))
        assert response.status_code == 200
        assert response.context_data['filter_form'] is not None

        table_data = list(response.context_data['table'].data.queryset.order_by('pk'))
        assert table_data == list(User.objects.all().order_by('pk'))

    def test_filter_active(self, user_rf):
        response = self.filtered_view(
            user_rf.get('/', data={'is_staff': False}, user=self.staff_user))
        assert response.status_code == 200

        table_data = list(response.context_data['table'].data.queryset)
        assert table_data == list(User.objects.filter(is_staff=False))


@pytest.mark.django_db
class TestAddView:

    def setup(self):
        self.view = CruditorAddView.as_view(
            model=User, fields=('username',), success_url='/add-success/')
        self.staff_user = UserFactory.create(is_staff=True)

    def test_get(self, user_rf, activate_en):
        response = self.view(user_rf.get('/', user=self.staff_user))
        assert response.status_code == 200
        assert response.template_name == ['cruditor/form.html']
        assert isinstance(response.context_data['form'].instance, User) is True
        assert response.context_data['form'].is_bound is False
        assert response.context_data['cruditor']['title'] == 'Add user'

    def test_form_invalid(self, user_rf, activate_en):
        response = self.view(user_rf.post('/', data={}, user=self.staff_user))
        assert response.status_code == 200
        form = response.context_data['form']
        assert form.is_valid() is False
        assert 'username' in form.errors
        assert User.objects.filter(is_staff=False).count() == 0

    def test_form_valid(self, user_rf, activate_en):
        response = self.view(user_rf.post(
            '/', data={'username': 'newuser'}, user=self.staff_user))
        assert response.status_code == 302
        assert response['Location'].endswith('/add-success/')
        assert User.objects.filter(is_staff=False).get().username == 'newuser'


@pytest.mark.django_db
class TestChangeView:

    def setup(self):
        self.view = CruditorChangeView.as_view(
            model=User, fields=('username',), success_url='/change-success/',
            formset_classes={'logentry_formset': inlineformset_factory(
                User, LogEntry, fields=('object_repr', 'action_flag'), extra=1
            )}
        )
        self.staff_user = UserFactory.create(is_staff=True)
        self.user = UserFactory.create(is_staff=False, username='existuser')

    def test_get(self, user_rf, activate_en):
        response = self.view(user_rf.get('/', user=self.staff_user), pk=self.user.pk)
        assert response.status_code == 200
        assert response.template_name == ['cruditor/form.html']
        assert isinstance(response.context_data['form'].instance, User) is True
        assert response.context_data['form'].instance.pk == self.user.pk
        assert response.context_data['form'].is_bound is False
        assert response.context_data['cruditor']['title'] == 'Change: existuser'

    def test_form_invalid(self, user_rf, activate_en):
        response = self.view(
            user_rf.post('/', data={
                'logentry_set-TOTAL_FORMS': 1,
                'logentry_set-INITIAL_FORMS': 0,
            }, user=self.staff_user), pk=self.user.pk)
        assert response.status_code == 200

        form = response.context_data['form']
        assert form.is_valid() is False
        assert 'username' in form.errors

        self.user.refresh_from_db()
        assert self.user.username == 'existuser'

    def test_form_valid(self, user_rf, activate_en):
        assert LogEntry.objects.filter(user=self.user).count() == 0
        response = self.view(user_rf.post(
            '/', data={
                'username': 'othername',
                'logentry_set-TOTAL_FORMS': 1,
                'logentry_set-INITIAL_FORMS': 0,
                'logentry_set-0-object_repr': 'Foobar',
                'logentry_set-0-action_flag': 1,
            }, user=self.staff_user), pk=self.user.pk)
        assert response.status_code == 302
        assert response['Location'].endswith('/change-success/')

        self.user.refresh_from_db()
        assert self.user.username == 'othername'
        entry = LogEntry.objects.get(user=self.user)
        assert entry.action_flag == 1
        assert entry.object_repr == 'Foobar'


@pytest.mark.django_db
class TestDeleteView:

    def setup(self):
        self.view = CruditorDeleteView.as_view(model=User, success_url='/delete-success/')
        self.staff_user = UserFactory.create(is_staff=True)
        self.user = UserFactory.create(is_staff=False, username='existuser')

    def test_get(self, user_rf, activate_en):
        response = self.view(user_rf.get('/', user=self.staff_user), pk=self.user.pk)
        assert response.status_code == 200
        assert response.template_name == ['cruditor/delete.html']
        assert response.context_data['form'].is_bound is False
        assert response.context_data['cruditor']['title'] == 'Delete: existuser'

    def test_form_invalid(self, user_rf, activate_en):
        response = self.view(
            user_rf.post('/', data={}, user=self.staff_user), pk=self.user.pk)
        assert response.status_code == 200

        form = response.context_data['form']
        assert form.is_valid() is False
        assert 'confirm' in form.errors

        assert User.objects.filter(is_staff=False).count() == 1

    def test_form_valid(self, user_rf, activate_en):
        response = self.view(user_rf.post(
            '/', data={'confirm': True}, user=self.staff_user), pk=self.user.pk)
        assert response.status_code == 302
        assert response['Location'].endswith('/delete-success/')

        assert User.objects.filter(is_staff=False).count() == 0


@pytest.mark.django_db
class TestChangePasswordView:

    def setup(self):
        self.view = CruditorChangePasswordView.as_view()
        self.staff_user = UserFactory.create(is_staff=True)

    def test_get(self, user_rf, activate_en):
        response = self.view(user_rf.get('/', user=self.staff_user))
        assert response.status_code == 200
        assert response.template_name == ['cruditor/change-password.html']
        assert response.context_data['form'].is_bound is False
        assert response.context_data['form'].user == self.staff_user
        assert response.context_data['cruditor']['title'] == 'Change password'

    def test_form_invalid(self, user_rf, activate_en):
        response = self.view(user_rf.post('/', data={}, user=self.staff_user))
        assert response.status_code == 200

        form = response.context_data['form']
        assert form.is_valid() is False
        assert 'new_password1' in form.errors
        assert 'new_password2' in form.errors

    def test_form_valid(self, user_rf, activate_en, client):
        assert client.login(username=self.staff_user.username, password='test') is False
        response = self.view(user_rf.post('/change-password/', data={
            'new_password1': 'test',
            'new_password2': 'test'
        }, user=self.staff_user))
        assert response.status_code == 302
        assert response['Location'].endswith('/change-password/')
        assert client.login(username=self.staff_user.username, password='test') is True


@pytest.mark.django_db
class TestLogoutView:

    def setup(self):
        self.view = CruditorLogoutView.as_view()
        self.staff_user = UserFactory.create(is_staff=True)

    def test_logout(self, user_rf):
        request = user_rf.get('/', user=self.staff_user)
        assert request.user.is_authenticated() is True
        response = self.view(request)
        assert response.status_code == 200
        assert response.template_name == 'cruditor/logout.html'
        assert request.user.is_authenticated() is False


@pytest.mark.django_db
class Test404View:

    def setup(self):
        self.view = Cruditor404View.as_view()
        self.staff_user = UserFactory.create(is_staff=True)

    def test_logged_in(self, user_rf):
        request = user_rf.get('/', user=self.staff_user)
        response = self.view(request)
        assert response.status_code == 404
        assert response.template_name == ['cruditor/404.html']

    def test_not_logged_in(self, user_rf):
        request = user_rf.get('/')
        response = self.view(request)
        assert response.status_code == 404
        assert response.template_name == ['cruditor/404.html']


@pytest.mark.django_db
class Test403View:

    def setup(self):
        self.view = Cruditor403View.as_view()
        self.staff_user = UserFactory.create(is_staff=True)

    def test_logged_in(self, user_rf):
        request = user_rf.get('/', user=self.staff_user)
        response = self.view(request)
        assert response.status_code == 403
        assert response.template_name == ['cruditor/403.html']

    def test_not_logged_in(self, user_rf):
        request = user_rf.get('/')
        response = self.view(request)
        assert response.status_code == 403
        assert response.template_name == ['cruditor/403.html']
