from django.urls import reverse, reverse_lazy

from cruditor.collection import CollectionViewMixin
from cruditor.views import (
    CruditorAddView, CruditorChangeView, CruditorDeleteView, CruditorListView)
from examples.mixins import ExamplesMixin
from examples.store.models import Person

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
    success_url = reverse_lazy('collection:list')
    form_class = PersonForm


class PersonChangeView(PersonViewMixin, CruditorChangeView):
    success_url = reverse_lazy('collection:list')
    form_class = PersonForm

    def get_delete_url(self):
        return reverse('collection:delete', args=(self.object.pk,))

    def get_success_message(self):
        return None


class PersonDeleteView(PersonViewMixin, CruditorDeleteView):
    success_url = reverse_lazy('collection:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_save_button_label'] = 'Delete this person'
        return context
