from django import forms
from cruditor.forms import CruditorTapeformMixin


class RecordForm(CruditorTapeformMixin, forms.Form):
    name = forms.CharField(label='Name', required=True)
    comment = forms.CharField(label='Comment', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
