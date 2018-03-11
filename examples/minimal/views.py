from cruditor.views import CruditorAddView, CruditorChangeView, CruditorDeleteView, CruditorListView
from django.urls import reverse

from examples.mixins import ExamplesMixin

from .forms import PersonForm
from .models import Person
from .tables import PersonTable


class PersonViewMixin(ExamplesMixin):
    model = Person


class PersonListView(PersonViewMixin, CruditorListView):
    title = 'Persons'
    table_class = PersonTable

    def get_titlebuttons(self):
        return [{'url': reverse('minimal:add'), 'label': 'Add person'}]


class PersonAddView(PersonViewMixin, CruditorAddView):
    form_class = PersonForm
    required_permission = 'nonexist'


class PersonChangeView(PersonViewMixin, CruditorChangeView):
    form_class = PersonForm

    def get_delete_url(self):
        return reverse('minimal:delete', args=(self.object.pk,))


class PersonDeleteView(PersonViewMixin, CruditorDeleteView):
    pass
