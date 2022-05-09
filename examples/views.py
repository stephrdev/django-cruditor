from django.views.generic import TemplateView

from cruditor.mixins import CruditorMixin
from cruditor.views import (
    Cruditor403View,
    Cruditor404View,
    CruditorChangePasswordView,
    CruditorLogoutView,
)

from .mixins import ExamplesMixin


class HomeView(ExamplesMixin, CruditorMixin, TemplateView):
    title = 'Welcome!'
    template_name = 'home.html'


class LogoutView(ExamplesMixin, CruditorLogoutView):
    pass


class ChangePasswordView(ExamplesMixin, CruditorChangePasswordView):
    pass


class ForbiddenView(ExamplesMixin, Cruditor403View):
    pass


class NotFoundView(ExamplesMixin, Cruditor404View):
    pass
