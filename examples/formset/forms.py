from cruditor.forms import CruditorFormsetFormMixin, CruditorFormsetMixin, CruditorTapeformMixin
from django import forms
from django.forms.models import inlineformset_factory

from examples.store.models import Person, RelatedPerson


class PersonForm(CruditorTapeformMixin, forms.ModelForm):
    reminder = forms.SplitDateTimeField()

    class Meta:
        model = Person
        fields = "__all__"


class RelatedPersonForm(CruditorFormsetFormMixin, forms.ModelForm):
    class Meta:
        model = RelatedPerson
        fields = "__all__"


class RelatedPersonFormset(
    CruditorFormsetMixin,
    inlineformset_factory(Person, RelatedPerson, extra=1, form=RelatedPersonForm),
):
    def __init__(self, *args, **kwargs):
        self.extra_kwarg = kwargs.pop("extra_kwarg", False)
        super().__init__(*args, **kwargs)
