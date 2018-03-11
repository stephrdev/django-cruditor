from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from tapeforms.mixins import TapeformMixin


class CruditorTapeformMixin(TapeformMixin):
    layout_template = 'cruditor/forms/layout.html'

    field_template = 'cruditor/forms/field.html'
    field_label_css_class = 'uk-form-label'

    widget_css_class = 'uk-input'
    widget_template_overrides = {
        forms.SelectDateWidget: 'cruditor/forms/widgets/multiwidget.html',
        forms.SplitDateTimeWidget: 'cruditor/forms/widgets/multiwidget.html',
        forms.RadioSelect: 'cruditor/forms/widgets/radioselect.html'
    }

    def get_widget_css_class(self, field_name, field):
        if isinstance(field.widget, (forms.Select,)):
            return 'uk-select'

        if isinstance(field.widget, (forms.Textarea,)):
            return 'uk-textarea'

        if isinstance(field.widget, (forms.CheckboxInput,)):
            return 'uk-checkbox'

        if isinstance(field.widget, (forms.RadioSelect,)):
            return 'uk-radio'

        if isinstance(field.widget, forms.SelectDateWidget):
            return 'uk-select'

        return super().get_widget_css_class(field_name, field)

    def apply_widget_template(self, field_name):
        super().apply_widget_template(field_name)

        widget = self.fields[field_name].widget

        if isinstance(widget, forms.DateInput):
            widget.input_type = 'date'

        if isinstance(widget, forms.TimeInput):
            widget.input_type = 'time'

        if isinstance(widget, forms.SplitDateTimeWidget):
            widget.widgets[0].input_type = 'date'
            widget.widgets[1].input_type = 'time'


class LoginForm(CruditorTapeformMixin, AuthenticationForm):
    pass


class ChangePasswordForm(CruditorTapeformMixin, SetPasswordForm):
    pass


class DeleteConfirmForm(CruditorTapeformMixin, forms.Form):
    confirm = forms.BooleanField(
        label=_('Are you sure you want to delete this item?'), required=True)
