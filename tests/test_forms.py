from django import forms
from django.forms.models import inlineformset_factory
from django_filters.fields import DateRangeField

from cruditor.forms import CruditorFormsetFormMixin, CruditorFormsetMixin, CruditorTapeformMixin
from examples.store.models import Person, RelatedPerson


class DummyForm(CruditorFormsetFormMixin, forms.ModelForm):
    class Meta:
        model = RelatedPerson
        exclude = '__all__'


class DummyFormWithDateRangeField(CruditorTapeformMixin, forms.Form):
    dt_range = DateRangeField()


class DummyFormset(
    CruditorFormsetMixin, inlineformset_factory(Person, RelatedPerson, extra=1, form=DummyForm)
):
    pass


class NoDeleteDummyFormset(
    CruditorFormsetMixin,
    inlineformset_factory(Person, RelatedPerson, extra=1, form=DummyForm, can_delete=False),
):
    pass


class JsOptionsDummyFormset(DummyFormset):
    js_formset_options = {'add-title': 'New one'}


class TemplateContextDummyFormset(DummyFormset):
    def get_template_context(self):
        context = super().get_template_context()
        context.update(
            {
                'form_headline_new_instance': 'New instance',
                'foo': 'bar',
            }
        )
        return context


def test_form_daterange_widget_input_types():
    form = DummyFormWithDateRangeField()
    assert form.fields['dt_range'].widget.widgets[0].input_type == 'date'
    assert form.fields['dt_range'].widget.widgets[1].input_type == 'date'


def test_formset_form_delete_field_hidden():
    form = DummyFormset().forms[0]
    assert 'DELETE' in list(form.fields)
    assert 'DELETE' not in form.visible_fields()
    assert 'DELETE' not in form.hidden_fields()
    assert form.fields['DELETE'].widget.is_hidden is True


def test_formset_form_delete_field_not_present():
    form = NoDeleteDummyFormset().forms[0]
    assert 'DELETE' not in list(form.fields)


def test_formset_js_options_default():
    formset = DummyFormset()
    assert formset.get_js_formset_options() == {
        'add-button-label': 'Add item',
        'add-title': 'New item',
        'delete-button-label': 'Delete item',
        'delete-confirm-text': 'Are you sure? Item will be deleted after saving.',
        'prefix': 'relatedperson_set',
    }


def test_formset_js_options_override():
    formset = JsOptionsDummyFormset()
    assert formset.get_js_formset_options() == {
        'add-button-label': 'Add item',
        'add-title': 'New one',
        'delete-button-label': 'Delete item',
        'delete-confirm-text': 'Are you sure? Item will be deleted after saving.',
        'prefix': 'relatedperson_set',
    }


def test_formset_template_context():
    formset = DummyFormset()
    assert formset.template_context == {'form_headline_new_instance': 'New item'}


def test_formset_template_context_with_content():
    formset = TemplateContextDummyFormset()
    assert formset.template_context == {
        'form_headline_new_instance': 'New instance',
        'foo': 'bar',
    }
