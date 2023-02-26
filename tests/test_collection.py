import django_tables2
import pytest
from django.views.generic import DetailView

from cruditor.mixins import CruditorMixin
from examples.collection.tables import PersonTable
from examples.collection.views import (
    PersonAddView,
    PersonChangeView,
    PersonDeleteView,
    PersonFilterView,
    PersonListView,
    PersonViewMixin,
)

from .factories import PersonFactory


class PersonDetailView(PersonViewMixin, CruditorMixin, DetailView):
    pass


class TestListView:
    def test_title(self):
        assert PersonListView().get_title() == 'Persons'

    def test_title_from_get_collection_list_title(self):
        class OtherListView(PersonListView):
            def get_collection_list_title(self):
                return 'Other title'

        assert OtherListView().get_title() == 'Other title'

    def test_breadcrumb(self):
        assert PersonListView().get_breadcrumb() == []

    def test_table_explicit(self):
        view = PersonFilterView()

        assert view.get_table_class() is PersonTable

    def test_table_fallback(self):
        view = PersonListView()

        table_class = view.get_table_class()
        assert issubclass(table_class, django_tables2.Table) is True

        table_class2 = view.get_table_class()
        assert table_class2 is table_class


class TestAddView:
    def setup_method(self):
        self.view = PersonAddView()
        self.view.object = None

    def test_title(self):
        assert self.view.get_title() == 'Add Person'

    def test_breadcrumb(self):
        assert self.view.get_breadcrumb() == [{'title': 'Persons', 'url': '/collection/'}]


@pytest.mark.django_db
class TestChangeView:
    def setup_method(self):
        self.view = PersonChangeView()
        self.view.object = PersonFactory.create(first_name='John')

    def test_title(self):
        assert self.view.get_title() == 'Change: John'

    def test_breadcrumb_title(self):
        assert self.view.get_breadcrumb_title() == 'Change: John'

    def test_breadcrumb(self):
        assert self.view.get_breadcrumb() == [{'title': 'Persons', 'url': '/collection/'}]


@pytest.mark.django_db
class TestDeleteView:
    def setup_method(self):
        self.view = PersonDeleteView()
        self.view.object = PersonFactory.create(first_name='John')

    def test_title(self):
        assert self.view.get_title() == 'Delete: John'

    def test_breadcrumb_title(self):
        assert self.view.get_breadcrumb_title() == 'Delete'

    def test_breadcrumb(self):
        assert self.view.get_breadcrumb() == [
            {'title': 'Persons', 'url': '/collection/'},
            {'title': 'John', 'url': '/collection/{}/'.format(self.view.object.pk)},
        ]


@pytest.mark.django_db
class TestDetailView:
    def setup_method(self):
        self.view = PersonDetailView()
        self.view.object = PersonFactory.create(first_name='John')

    def test_breadcrumb_no_object(self):
        del self.view.object
        assert self.view.get_breadcrumb() == [
            {'title': 'Persons', 'url': '/collection/'},
        ]

    def test_breadcrumb(self):
        assert self.view.get_breadcrumb() == [
            {'title': 'Persons', 'url': '/collection/'},
            {'title': 'John', 'url': '/collection/1/'},
        ]
