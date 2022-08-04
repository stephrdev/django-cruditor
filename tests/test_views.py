import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import SUCCESS as SUCCESS_LEVEL
from django.contrib.messages import get_messages
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.urls import reverse

from cruditor.views import Cruditor403View, Cruditor404View, CruditorListView
from examples.minimal.views import DemoView
from examples.store.models import Person

from .factories import PersonFactory, RelatedPersonFactory


@pytest.mark.django_db
class TestBasicView:
    @pytest.fixture(autouse=True)
    def setup(self, rf, admin_user):
        self.request = rf.get('/')
        self.request.user = admin_user
        self.view = DemoView()
        self.view.request = self.request
        self.view.required_permission = 'accounts.some_permission'

    def test_not_logged_in(self, rf):
        self.request.user = AnonymousUser()
        response = self.view.dispatch(self.request)
        assert response.status_code == 200
        assert 'breadcrumb' not in response.context_data['cruditor']
        assert response.template_name[0] == DemoView.login_template_name

    def test_no_permission(self, admin_user):
        self.request.user.is_superuser = False
        with pytest.raises(PermissionDenied):
            self.view.dispatch(self.request)

    def test_no_permission_required(self, admin_user):
        self.view.required_permission = None
        self.request.user.is_superuser = False
        response = self.view.dispatch(self.request)
        assert response.status_code == 200

    def test_permission_granted(self, admin_user):
        response = self.view.dispatch(self.request)
        assert response.status_code == 200
        assert response.template_name[0] == 'minimal/demo.html'

    def test_cruditor_context(self):
        assert self.view.get_cruditor_context() == {
            'breadcrumb': [
                {'title': 'Additional breadcrumb', 'url': '/'},
                {'title': 'Disabled item'},
                {'title': 'Demo view', 'url': None},
            ],
            'constants': {
                'change_password_url': '/change-password/',
                'extrahead_template_name': 'cruditor/includes/extrahead.html',
                'index_url': '/',
                'logout_url': '/logout/',
                'menu_template_name': 'menu.html',
                'menu_title': 'Examples Demo',
            },
            'title': 'Demo view',
            'titlebuttons': None,
        }

    def test_title(self):
        assert self.view.get_title() == 'Demo view'

    def test_model_verbose_name_explicit(self):
        self.view.model_verbose_name = 'Foo'
        assert self.view.get_model_verbose_name() == 'Foo'

    def test_model_verbose_name_from_meta(self):
        self.view.model = Person
        assert self.view.get_model_verbose_name() == 'Person'

    def test_model_verbose_name_fallback(self):
        assert self.view.get_model_verbose_name() == 'Item'


def test_not_found_view(rf):
    response = Cruditor404View.as_view()(rf.get('/'))
    assert response.status_code == 404
    assert response.template_name[0] == 'cruditor/404.html'


def test_forbidden_view(rf):
    response = Cruditor403View.as_view()(rf.get('/'))
    assert response.status_code == 403
    assert response.template_name[0] == 'cruditor/403.html'


@pytest.mark.django_db
class TestListView:
    def setup(self):
        self.person1 = PersonFactory.create(approved=True)
        self.person2 = PersonFactory.create(approved=False)

    def test_get_without_filter(self, admin_client):
        response = admin_client.get(reverse('collection:list'))
        assert response.status_code == 200
        assert response.context['table'].data.data.count() == 2
        assert response.context['filter_form'] is None

    def test_get_with_filter(self, admin_client):
        response = admin_client.get(reverse('collection:filter'))
        assert response.status_code == 200
        assert response.context['table'].data.data.count() == 2
        assert response.context['filter_form'] is not None
        assert not response.context['filter_form'].data

    def test_get_with_filter_active(self, admin_client):
        response = admin_client.get(reverse('collection:filter'), data={'approved': '2'})
        assert response.status_code == 200
        assert response.context['table'].data.data.count() == 1
        assert response.context['filter_form'] is not None
        assert response.context['filter_form'].data

    def test_get_queryset_model(self):
        class DummyListView(CruditorListView):
            model = Person

        assert list(DummyListView().get_queryset()) == list(Person.objects.all())

    def test_get_queryset_qset(self):
        class DummyListView(CruditorListView):
            queryset = Person.objects.filter(approved=True)

        assert DummyListView().get_queryset().get() == self.person1

    def test_get_queryset_fallback(self):
        class DummyListView(CruditorListView):
            pass

        assert DummyListView().get_queryset() == []

    def test_get_table_class(self):
        class DummyListView(CruditorListView):
            table_class = object

        assert DummyListView().get_table_class()

    def test_get_table_class_invalid(self):
        class DummyListView(CruditorListView):
            pass

        with pytest.raises(ImproperlyConfigured):
            DummyListView().get_table_class()


@pytest.mark.django_db
class TestAddView:
    def test_get(self, admin_client):
        response = admin_client.get(reverse('collection:add'))
        assert response.status_code == 200
        assert response.context['cruditor']['title'] == 'Add Person'

    def test_post_valid(self, admin_client):
        response = admin_client.post(
            reverse('collection:add'),
            data={
                'first_name': 'John',
                'last_name': 'Doe',
                'country': 'Germany',
                'reminder_0': '2018-05-25',
                'reminder_1': '09:00:00',
                'stars': '2',
            },
        )
        assert response.status_code == 302
        assert response['Location'] == reverse('collection:list')

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert messages[0].level == SUCCESS_LEVEL

        assert Person.objects.get().first_name == 'John'

    def test_post_invalid(self, admin_client):
        response = admin_client.post(reverse('collection:add'), data={})
        assert response.status_code == 200
        assert response.context['form'].is_valid() is False

        assert Person.objects.exists() is False


@pytest.mark.django_db
class TestChangeView:
    def setup(self):
        self.person = PersonFactory.create(first_name='Sally')

    def test_get(self, admin_client):
        response = admin_client.get(reverse('collection:change', args=(self.person.pk,)))
        assert response.status_code == 200
        assert response.context['form'].instance == self.person

    def test_post_valid(self, admin_client):
        response = admin_client.post(
            reverse('collection:change', args=(self.person.pk,)),
            data={
                'first_name': 'John',
                'last_name': 'Doe',
                'country': 'Germany',
                'reminder_0': '2018-05-25',
                'reminder_1': '09:00:00',
                'stars': '2',
            },
        )
        assert response.status_code == 302
        assert response['Location'] == reverse('collection:list')

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 0

        self.person.refresh_from_db()
        assert self.person.first_name == 'John'

    def test_post_invalid(self, admin_client):
        response = admin_client.post(
            reverse('collection:change', args=(self.person.pk,)), data={}
        )
        assert response.status_code == 200
        assert response.context['form'].is_valid() is False

        assert Person.objects.get().first_name == 'Sally'


@pytest.mark.django_db
class TestDeleteView:
    def setup(self):
        self.person = PersonFactory.create(first_name='Sally')

    def test_get(self, admin_client):
        response = admin_client.get(reverse('collection:delete', args=(self.person.pk,)))
        assert response.status_code == 200

        assert Person.objects.exists() is True

    def test_post(self, admin_client):
        response = admin_client.post(reverse('collection:delete', args=(self.person.pk,)))
        assert response.status_code == 302
        assert response['Location'] == reverse('collection:list')

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert messages[0].level == SUCCESS_LEVEL

        assert Person.objects.exists() is False

    def test_post_protected(self, admin_client):
        related = RelatedPersonFactory(person=self.person)

        response = admin_client.post(reverse('collection:delete', args=(self.person.pk,)))
        assert response.status_code == 200
        assert response.context['linked_objects'] == [
            'Related person: {}'.format(str(related)),
        ]

        assert Person.objects.exists() is True

    def test_custom_button_label(self, admin_client):
        response = admin_client.get(reverse('collection:delete', args=(self.person.pk,)))
        assert response.context['form_save_button_label'] == 'Delete this person'
        assert 'Delete this person' in response.content.decode(response.charset)


@pytest.mark.django_db
class TestFormsetView:
    def setup(self):
        self.person = PersonFactory.create()
        self.related_persons = RelatedPersonFactory.create_batch(2, person=self.person)

    def test_get(self, admin_client):
        response = admin_client.get(reverse('formset:change', args=(self.person.pk,)))
        assert response.status_code == 200
        assert response.context['form'].instance == self.person
        assert response.context['formsets']['related_persons'].extra_kwarg == 'extra'

        instances = [
            form.instance for form in response.context['formsets']['related_persons'].forms
        ]
        assert self.related_persons[0] in instances
        assert self.related_persons[1] in instances

    def test_post_valid(self, admin_client):
        response = admin_client.post(
            reverse('formset:change', args=(self.person.pk,)),
            data={
                'first_name': 'John',
                'last_name': 'Doe',
                'country': 'Germany',
                'reminder_0': '2018-05-25',
                'reminder_1': '09:00:00',
                'stars': '2',
                'relatedperson_set-INITIAL_FORMS': '1',
                'relatedperson_set-MAX_NUM_FORMS': '1000',
                'relatedperson_set-MIN_NUM_FORMS': '0',
                'relatedperson_set-TOTAL_FORMS': '1',
                'relatedperson_set-0-DELETE': '',
                'relatedperson_set-0-id': '1',
                'relatedperson_set-0-first_name': 'Sally',
                'relatedperson_set-0-last_name': 'Mary',
                'relatedperson_set-0-person': '1',
            },
        )
        assert response.status_code == 302
        assert response['Location'] == reverse('formset:list')

        self.person.refresh_from_db()
        assert self.person.first_name == 'John'
        self.related_persons[0].refresh_from_db()
        assert self.related_persons[0].first_name == 'Sally'

    def test_post_invalid_formset(self, admin_client):
        response = admin_client.post(
            reverse('formset:change', args=(self.person.pk,)),
            data={
                'first_name': 'John',
                'last_name': 'Doe',
                'country': 'Germany',
                'reminder_0': '2018-05-25',
                'reminder_1': '09:00:00',
                'stars': '2',
                'relatedperson_set-INITIAL_FORMS': '1',
                'relatedperson_set-MAX_NUM_FORMS': '1000',
                'relatedperson_set-MIN_NUM_FORMS': '0',
                'relatedperson_set-TOTAL_FORMS': '1',
                'relatedperson_set-0-DELETE': '',
                'relatedperson_set-0-id': '1',
                'relatedperson_set-0-first_name': '',
                'relatedperson_set-0-last_name': '',
                'relatedperson_set-0-person': '1',
            },
        )
        assert response.status_code == 200
        assert response.context['form'].is_valid() is True
        assert response.context['formsets']['related_persons'].is_valid() is False

    def test_post_invalid_form(self, admin_client):
        response = admin_client.post(
            reverse('formset:change', args=(self.person.pk,)),
            data={
                'first_name': '',
                'last_name': '',
                'country': 'Germany',
                'reminder_0': '2018-05-25',
                'reminder_1': '09:00:00',
                'stars': '2',
                'relatedperson_set-INITIAL_FORMS': '1',
                'relatedperson_set-MAX_NUM_FORMS': '1000',
                'relatedperson_set-MIN_NUM_FORMS': '0',
                'relatedperson_set-TOTAL_FORMS': '1',
                'relatedperson_set-0-DELETE': '',
                'relatedperson_set-0-id': '1',
                'relatedperson_set-0-first_name': 'Sally',
                'relatedperson_set-0-last_name': 'Mary',
                'relatedperson_set-0-person': '1',
            },
        )
        assert response.status_code == 200
        assert response.context['form'].is_valid() is False
        assert response.context['formsets']['related_persons'].extra_kwarg is False
        assert response.context['formsets']['related_persons'].is_valid() is True


class TestChangePasswordView:
    def test_get(self, admin_client):
        response = admin_client.get(reverse('change-password'))
        assert response.status_code == 200
        assert list(response.context['form'].fields) == ['new_password1', 'new_password2']

    def test_post_invalid(self, admin_user, admin_client):
        response = admin_client.post(
            reverse('change-password'),
            data={'new_password1': 'Secret', 'new_password2': 'Secret2'},
        )
        assert response.status_code == 200
        assert response.context['form'].is_valid() is False

        admin_user.refresh_from_db()
        assert admin_user.check_password('password') is True

    def test_post_valid(self, admin_user, admin_client):
        response = admin_client.post(
            reverse('change-password'),
            data={'new_password1': 'Secret', 'new_password2': 'Secret'},
        )
        assert response.status_code == 302
        assert response['Location'] == reverse('change-password')

        admin_user.refresh_from_db()
        assert admin_user.check_password('Secret') is True


class TestLogoutView:
    def test_logout(self, admin_client):
        response = admin_client.get(reverse('minimal:demo'))
        assert response.status_code == 200
        assert response.template_name[0] == 'minimal/demo.html'

        response = admin_client.get(reverse('logout'))
        assert response.status_code == 200
        assert response.template_name[0] == 'cruditor/logout.html'

        response = admin_client.get(reverse('minimal:demo'))
        assert response.status_code == 200
        assert response.template_name[0] == 'cruditor/login.html'

    def test_logout_already_logged_out(self, client):
        response = client.get(reverse('logout'))
        assert response.status_code == 200
        assert response.template_name[0] == 'cruditor/logout.html'
