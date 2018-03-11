from cruditor.views import CruditorAddView, CruditorListView
from django.urls import reverse_lazy

from examples.mixins import ExamplesMixin

from .forms import RecordForm
from .tables import RecordTable


RECORD_STORE = []


class RecordListView(ExamplesMixin, CruditorListView):
    title = 'Records'
    table_class = RecordTable

    def get_queryset(self):
        global RECORD_STORE
        return RECORD_STORE


class RecordAddView(ExamplesMixin, CruditorAddView):
    success_url = reverse_lazy('remote:list')
    form_class = RecordForm
    title = 'Add record'

    def save_form(self, form):
        global RECORD_STORE
        RECORD_STORE.append(form.cleaned_data)
