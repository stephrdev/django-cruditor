from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from tapeforms.contrib.bootstrap import BootstrapTapeformMixin


class CruditorTapeformMixin(BootstrapTapeformMixin):
    pass


class LoginForm(CruditorTapeformMixin, AuthenticationForm):
    pass


class ChangePasswordForm(CruditorTapeformMixin, SetPasswordForm):
    pass


class DeleteConfirmForm(CruditorTapeformMixin, forms.Form):
    confirm = forms.BooleanField(
        label=_('Are you sure you want to delete this item?'), required=True)
