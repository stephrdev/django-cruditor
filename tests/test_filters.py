from cruditor.filters import AnyChoiceFilter, MultiCharFilter
from examples.store.models import Person


class TestAnyChoiceFilter:

    def test_default_label(self):
        instance = AnyChoiceFilter('foo')
        assert str(instance.extra['empty_label']) == 'Any choice'

    def test_custom_label(self):
        instance = AnyChoiceFilter('foo', empty_label='Anyting')
        assert str(instance.extra['empty_label']) == 'Anyting'


class TestMultiCharFilter:

    def test_init(self):
        instance = MultiCharFilter(('foo', 'bar'))
        assert instance.fields == ('foo', 'bar')

    def test_filter(self):
        instance = MultiCharFilter(('first_name', '^last_name'))
        filters = instance.filter(
            Person.objects.all(), 'foo').query.has_filters().children[0].children
        assert filters[0].lhs.field.name == 'first_name'
        assert filters[0].lookup_name == 'icontains'

        assert filters[1].lhs.field.name == 'last_name'
        assert filters[1].lookup_name == 'istartswith'

    def test_skip_filter(self):
        instance = MultiCharFilter(('first_name', '^last_name'))
        assert len(instance.filter(
            Person.objects.all(), '').query.has_filters().children) == 0
