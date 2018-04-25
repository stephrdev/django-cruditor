from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.forms.formsets import DELETION_FIELD_NAME
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from tapeforms.contrib.bootstrap import BootstrapTapeformMixin


class CruditorTapeformMixin(BootstrapTapeformMixin):
    pass


class CruditorFormsetMixin(object):
    js_formset_options = None

    def add_fields(self, form, index):
        super().add_fields(form, index)

        if DELETION_FIELD_NAME in form.fields:
            form.fields[DELETION_FIELD_NAME].widget = forms.HiddenInput()

    def get_js_formset_options(self):
        options = {
            'prefix': self.prefix,
            'add-button-label': ugettext('Add another'),
            'add-title': ugettext('New item'),
            'delete-button-label': ugettext('Delete item'),
            'delete-confirm-text': ugettext(
                'Are you sure? Item will be deleted after saving.')
        }
        options.update(self.js_formset_options or {})
        return options


class CruditorFormsetFormMixin(CruditorTapeformMixin):

    def visible_fields(self):
        return [field for field in super().visible_fields() if field.name != 'DELETE']


class LoginForm(CruditorTapeformMixin, AuthenticationForm):
    pass


class ChangePasswordForm(CruditorTapeformMixin, SetPasswordForm):
    pass


class DeleteConfirmForm(CruditorTapeformMixin, forms.Form):
    confirm = forms.BooleanField(
        label=_('Are you sure you want to delete this item?'), required=True)
