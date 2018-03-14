from django import forms

from cruditor.forms import CruditorTapeformMixin
from store.models import Person


class PersonForm(CruditorTapeformMixin, forms.ModelForm):
    reminder = forms.SplitDateTimeField(label='Next reminder')

    class Meta:
        model = Person
        fields = '__all__'
