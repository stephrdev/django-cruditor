import django_tables2 as tables
from django_tables2.utils import A

from examples.store.models import Person


class PersonTable(tables.Table):
    first_name = tables.LinkColumn('collection:change', args=(A('pk'),))

    class Meta:
        model = Person
        fields = ('first_name', 'reminder')
