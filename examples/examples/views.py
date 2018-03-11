from cruditor.views import Cruditor403View, Cruditor404View, CruditorChangePasswordView, CruditorLogoutView

from .mixins import ExamplesMixin


class LogoutView(ExamplesMixin, CruditorLogoutView):
    pass


class ChangePasswordView(ExamplesMixin, CruditorChangePasswordView):
    pass


class ForbiddenView(ExamplesMixin, Cruditor403View):
    pass


class NotFoundView(ExamplesMixin, Cruditor404View):
    pass
