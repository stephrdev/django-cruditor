import floppyforms.__future__ as forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _


class LoginForm(AuthenticationForm, forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class ChangePasswordForm(SetPasswordForm, forms.Form):
    new_password1 = forms.CharField(
        label=_('New password'), widget=forms.PasswordInput)
    new_password2 = forms.CharField(
        label=_('New password confirmation'), widget=forms.PasswordInput)


class DeleteConfirmForm(forms.Form):
    confirm = forms.BooleanField(
        label=_('Are you sure you want to delete this item?'), required=True)
