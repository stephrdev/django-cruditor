from django import forms
from cruditor.forms import CruditorTapeformMixin

from .models import Pet


class PetForm(CruditorTapeformMixin, forms.Form):
    name = forms.CharField(label='Name', required=True)
    photo_url = forms.URLField(label='Photo URL', required=True)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        if self.instance:
            kwargs['initial'] = self.instance.for_form()
        super().__init__(*args, **kwargs)

    def save(self):
        if self.instance:
            self.instance.update(self.cleaned_data)
        else:
            self.instance = Pet.create(self.cleaned_data)

        return self.instance
