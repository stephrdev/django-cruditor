import django_tables2 as tables
from django.contrib.auth.models import User
from django_tables2.utils import A



class UserTable(tables.Table):
    username = tables.LinkColumn('user-change', args=[A('pk')])

    class Meta:
        model = User
        per_page = 10
        fields = ('username', 'first_name', 'last_name', 'is_active')
