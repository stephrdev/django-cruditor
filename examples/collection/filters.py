import django_filters
from django import forms

from cruditor.filters import AnyChoiceFilter, MultiCharFilter
from cruditor.forms import CruditorTapeformMixin
from examples.store.models import Person


class PersonFilter(django_filters.FilterSet):
    search = MultiCharFilter(
        ('first_name', 'last_name'),
        label='Search',
        help_text=('Search for first or last name.'),
    )
    country = AnyChoiceFilter(
        choices=zip(Person.COUNTRIES, Person.COUNTRIES), widget=forms.RadioSelect
    )

    class Meta:
        model = Person
        fields = ('search', 'country', 'approved')

        class form(CruditorTapeformMixin, forms.Form):
            pass
