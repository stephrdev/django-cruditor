from django import forms
from cruditor.forms import CruditorTapeformMixin

from .models import Person


class PersonForm(CruditorTapeformMixin, forms.ModelForm):
    reminder = forms.SplitDateTimeField(label='Next reminder')

    class Meta:
        model = Person
        fields = '__all__'
        widgets = {
            'stars': forms.RadioSelect,
            'birthdate': forms.SelectDateWidget,
        }
