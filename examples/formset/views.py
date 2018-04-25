from django.urls import reverse, reverse_lazy

from cruditor.contrib.collection import CollectionViewMixin
from cruditor.views import CruditorAddView, CruditorChangeView, CruditorListView
from examples.mixins import ExamplesMixin
from store.models import Person

from .forms import PersonForm, RelatedPersonFormset


class PersonViewMixin(ExamplesMixin, CollectionViewMixin):
    model = Person
    collection_list_title = 'Persons'
    collection_list_urlname = 'formset:list'
    collection_detail_urlname = 'formset:change'


class PersonListView(PersonViewMixin, CruditorListView):
    title = 'Persons'

    def get_titlebuttons(self):
        return [{'url': reverse('formset:add'), 'label': 'Add person'}]


class PersonAddView(PersonViewMixin, CruditorAddView):
    success_url = reverse_lazy('formset:list')
    form_class = PersonForm


class PersonChangeView(PersonViewMixin, CruditorChangeView):
    success_url = reverse_lazy('formset:list')
    form_class = PersonForm
    formset_classes = {
        'related_persons': RelatedPersonFormset
    }
