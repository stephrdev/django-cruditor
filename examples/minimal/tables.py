import django_tables2 as tables
from django_tables2.utils import A

from .models import Person


class PersonTable(tables.Table):
    first_name = tables.LinkColumn('minimal:change', args=(A('pk'),))

    class Meta:
        model = Person
        fields = ('first_name', 'reminder')
