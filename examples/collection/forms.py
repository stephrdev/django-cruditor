from django import forms

from cruditor.forms import CruditorTapeformMixin
from examples.store.models import Person


class PersonForm(CruditorTapeformMixin, forms.ModelForm):
    reminder = forms.SplitDateTimeField(label='Next reminder', help_text='Some help for you')

    fieldsets = [
        {"title": "The person", "fields": (("first_name", "last_name"), "birthdate")},
        {"exclude": ("first_name", "last_name", "birthdate")}
    ]

    class Meta:
        model = Person
        fields = '__all__'

    def clean(self):
        if not self.cleaned_data.get('last_name', ''):
            raise forms.ValidationError('Please provide a last name too.')

        return self.cleaned_data
