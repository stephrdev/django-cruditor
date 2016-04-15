from cruditor.widgets import (
    CruditorAutoSlugWidget, CruditorSelectMultiple, CruditorSplitDateTimeWidget)


class TestCruditorSplitDateTimeWidget:

    def test_init(self):
        widget = CruditorSplitDateTimeWidget()
        for wid in widget.widgets:
            assert wid.template_name == 'cruditor/forms/input.html'

    def test_format_output(self):
        widget = CruditorSplitDateTimeWidget()
        assert widget.format_output(['date', 'time']) == (
            '<div class="row"><div class="col-xs-6">date</div>'
            '<div class="col-xs-6">time</div></div>'
        )


class TestCruditorAutoSlugWidget:

    def test_init_defaults(self):
        widget = CruditorAutoSlugWidget(autoslug='foobar')
        assert widget.attrs == {
            'data-autoslug': 'foobar',
            'class': 'slugify'
        }

    def test_init_attrs(self):
        widget = CruditorAutoSlugWidget(autoslug='foobar', attrs={'foo': 'bar'})
        assert widget.attrs == {
            'foo': 'bar',
            'data-autoslug': 'foobar',
            'class': 'slugify'
        }


class TestCruditorSelectMultiple:

    def test_init_defaults(self):
        widget = CruditorSelectMultiple()
        assert widget.attrs == {
            'class': 'select2-multiple'
        }

    def test_init_attrs(self):
        widget = CruditorSelectMultiple(attrs={'foo': 'bar'})
        assert widget.attrs == {
            'foo': 'bar',
            'class': 'select2-multiple'
        }
