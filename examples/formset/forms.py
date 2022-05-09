from django import forms
from django.forms.models import inlineformset_factory

from cruditor.forms import CruditorFormsetFormMixin, CruditorFormsetMixin, CruditorTapeformMixin
from examples.store.models import Person, RelatedPerson


class PersonForm(CruditorTapeformMixin, forms.ModelForm):
    reminder = forms.SplitDateTimeField()

    class Meta:
        model = Person
        fields = '__all__'


class RelatedPersonForm(CruditorFormsetFormMixin, forms.ModelForm):
    class Meta:
        model = RelatedPerson
        fields = '__all__'


class RelatedPersonFormset(
    CruditorFormsetMixin,
    inlineformset_factory(Person, RelatedPerson, extra=1, form=RelatedPersonForm),
):
    pass
