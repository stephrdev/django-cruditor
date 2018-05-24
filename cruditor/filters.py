import functools
import operator

from django.db.models import Q
from django.utils.translation import ugettext
from django_filters import CharFilter, ChoiceFilter


class AnyChoiceFilter(ChoiceFilter):
    """
    Extended ChoiceFilter which adds an "any" choice to the choices from the
    field / provided options by setting a empty_label on the generated form field.
    """

    def __init__(self, *args, **kwargs):
        empty_label = kwargs.pop('empty_label', ugettext('Any choice'))
        super().__init__(*args, **kwargs)
        self.extra['empty_label'] = empty_label


class MultiCharFilter(CharFilter):
    """
    This filter performs an OR query on the defined fields from a
    single entered value.

    The following will work similar to the default UserAdmin search::

        class UserFilterSet(FilterSet):
            search = MultiCharFilter([
                'username', 'first_name', 'last_name', '^email'])

            class Meta:
                model = User
                fields = ['search']

    The filter supports filtering in different modes (icontains, istartswith,
    iexact, and search). icontains is the default mode, use ^, = and @ in the
    list of fields for the other modes.

    Based on some ideas from https://gist.github.com/nkryptic/4727865
    """
    default_lookup_type = 'icontains'
    lookup_types = [
        ('^', 'istartswith'),
        ('=', 'iexact'),
        ('@', 'search'),
    ]

    def __init__(self, fields, *args, **kwargs):
        self.fields = fields
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not self.fields or not value:
            return qs

        lookups = [self._get_lookup(str(field)) for field in self.fields]
        queries = [Q(**{lookup: value}) for lookup in lookups]
        qs = qs.filter(functools.reduce(operator.or_, queries))
        return qs

    def _get_lookup(self, field_name):
        for key, lookup_type in self.lookup_types:
            if field_name.startswith(key):
                return '{0}__{1}'.format(field_name[len(key):], lookup_type)
        return '{0}__{1}'.format(field_name, self.default_lookup_type)
