import django_tables2
import pytest
from cruditor.collection import generate_urls
from cruditor.datastructures import Breadcrumb
from cruditor.mixins import CruditorMixin
from django.views.generic import DetailView
from examples.collection.tables import PersonTable
from examples.collection.views import (
    PersonAddView,
    PersonChangeView,
    PersonDeleteView,
    PersonFilterView,
    PersonListView,
    PersonViewMixin,
)

from tests.factories import PersonFactory


class PersonDetailView(PersonViewMixin, CruditorMixin, DetailView):
    pass


class TestListView:
    def test_title(self):
        assert PersonListView().get_title() == "Persons"

    def test_title_from_get_collection_list_title(self):
        class OtherListView(PersonListView):
            def get_collection_list_title(self):
                return "Other title"

        assert OtherListView().get_title() == "Other title"

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
        assert self.view.get_title() == "Add Person"

    def test_breadcrumb(self):
        assert self.view.get_breadcrumb() == [Breadcrumb(title="Persons", url="/collection/")]


@pytest.mark.django_db
class TestChangeView:
    def setup_method(self):
        self.view = PersonChangeView()
        self.view.object = PersonFactory.create(first_name="John")

    def test_title(self):
        assert self.view.get_title() == "Change: John"

    def test_breadcrumb_title(self):
        assert self.view.get_breadcrumb_title() == "Change: John"

    def test_breadcrumb(self):
        assert self.view.get_breadcrumb() == [Breadcrumb(title="Persons", url="/collection/")]


@pytest.mark.django_db
class TestDeleteView:
    def setup_method(self):
        self.view = PersonDeleteView()
        self.view.object = PersonFactory.create(first_name="John")

    def test_title(self):
        assert self.view.get_title() == "Delete: John"

    def test_breadcrumb_title(self):
        assert self.view.get_breadcrumb_title() == "Delete"

    def test_breadcrumb(self):
        assert self.view.get_breadcrumb() == [
            Breadcrumb(title="Persons", url="/collection/"),
            Breadcrumb(title="John", url=f"/collection/{self.view.object.pk}/"),
        ]


@pytest.mark.django_db
class TestDetailView:
    def setup_method(self):
        self.view = PersonDetailView()
        self.view.object = PersonFactory.create(first_name="John")

    def test_breadcrumb_no_object(self):
        del self.view.object
        assert self.view.get_breadcrumb() == [
            Breadcrumb(title="Persons", url="/collection/"),
        ]

    def test_breadcrumb(self):
        assert self.view.get_breadcrumb() == [
            Breadcrumb(title="Persons", url="/collection/"),
            Breadcrumb(title="John", url=f"/collection/{self.view.object.pk}/"),
        ]


class TestGenerateUrls:
    def test_basic(self):
        urls = generate_urls("", "", PersonListView, PersonAddView, PersonChangeView)
        assert len(urls) == 3
        assert urls[0].name == "list"
        assert urls[0].callback.view_class is PersonListView
        assert urls[0].pattern._route == ""
        assert urls[1].name == "add"
        assert urls[1].callback.view_class is PersonAddView
        assert urls[1].pattern._route == "add/"
        assert urls[2].name == "change"
        assert urls[2].callback.view_class is PersonChangeView
        assert urls[2].pattern._route == "<int:pk>/"

    def test_extra_no_slashes(self, settings):
        settings.APPEND_SLASH = False
        urls = generate_urls(
            "",
            "",
            PersonListView,
            change_view=PersonChangeView,
            extra_detail_views={"removal": PersonDeleteView},
        )
        assert len(urls) == 3
        assert urls[0].name == "list"
        assert urls[0].callback.view_class is PersonListView
        assert urls[0].pattern._route == ""
        assert urls[1].name == "change"
        assert urls[1].callback.view_class is PersonChangeView
        assert urls[1].pattern._route == "<int:pk>"
        assert urls[2].name == "removal"
        assert urls[2].callback.view_class is PersonDeleteView
        assert urls[2].pattern._route == "<int:pk>/removal"
