from cruditor.collection import CollectionViewMixin
from cruditor.views import (
    CruditorAddView,
    CruditorChangeView,
    CruditorDeleteView,
    CruditorListView,
)
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy

from examples.mixins import ExamplesMixin
from examples.store.models import Person

from .filters import PersonFilter
from .forms import PersonForm
from .tables import PersonTable


class PersonViewMixin(ExamplesMixin, CollectionViewMixin):
    model = Person
    collection_list_title = "Persons"
    collection_list_urlname = "collection:list"
    collection_add_urlname = "collection:add"
    collection_detail_urlname = "collection:change"
    collection_delete_urlname = "collection:delete"


class PersonListView(PersonViewMixin, CruditorListView):
    title = "Persons"


class PersonFilterView(PersonListView):
    filter_class = PersonFilter
    table_class = PersonTable


class PersonAddView(PersonViewMixin, CruditorAddView):
    form_class = PersonForm


class PersonChangeView(PersonViewMixin, CruditorChangeView):
    form_class = PersonForm

    def get_success_message(self):
        return None


class PersonDeleteView(PersonViewMixin, CruditorDeleteView):
    form_save_button_label = "Delete this person"
