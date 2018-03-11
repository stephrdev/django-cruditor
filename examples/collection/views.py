from cruditor.contrib.collection import CollectionViewMixin
from cruditor.views import CruditorAddView, CruditorChangeView, CruditorDeleteView, CruditorListView
from django.urls import reverse, reverse_lazy

from examples.mixins import ExamplesMixin
from store.models import Person

from .filters import PersonFilter
from .forms import PersonForm
from .tables import PersonTable


class PersonViewMixin(ExamplesMixin, CollectionViewMixin):
    model = Person
    collection_list_title = 'Persons'
    collection_list_urlname = 'collection:list'
    collection_detail_urlname = 'collection:change'


class PersonListView(PersonViewMixin, CruditorListView):
    title = 'Persons'

    def get_titlebuttons(self):
        return [{'url': reverse('collection:add'), 'label': 'Add person'}]


class PersonFilterView(PersonListView):
    filter_class = PersonFilter
    table_class = PersonTable


class PersonAddView(PersonViewMixin, CruditorAddView):
    success_url = reverse_lazy('collection:lits')
    form_class = PersonForm


class PersonChangeView(PersonViewMixin, CruditorChangeView):
    form_class = PersonForm

    def get_delete_url(self):
        return reverse('collection:delete', args=(self.object.pk,))


class PersonDeleteView(PersonViewMixin, CruditorDeleteView):
    pass
