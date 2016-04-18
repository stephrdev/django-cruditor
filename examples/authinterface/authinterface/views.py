from cruditor.views import (
    Cruditor403View, Cruditor404View, CruditorChangeView, CruditorListView,
    CruditorLogoutView)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy

from .forms import UserForm
from .tables import UserTable


class AuthInterfaceMixin(object):
    menu_title = 'Auth interface'
    index_url = reverse_lazy('user-list')
    logout_url = reverse_lazy('logout')
    staff_required = False


class NotFoundView(AuthInterfaceMixin, Cruditor404View):
    pass

not_found_view = NotFoundView.as_view()


class NoPermissionView(AuthInterfaceMixin, Cruditor403View):
    pass

no_permission_view = NoPermissionView.as_view()


class LogoutView(AuthInterfaceMixin, CruditorLogoutView):
    pass


class UserListView(AuthInterfaceMixin, CruditorListView):
    title = 'Users'
    model = User
    table_class = UserTable
    required_permission = 'auth.change_user'


class UserChangeView(AuthInterfaceMixin, CruditorChangeView):
    model = User
    form_class = UserForm
    required_permission = 'auth.change_user'

    def get_breadcrumb(self):
        return super().get_breadcrumb() + [
            {'title': 'Users', 'url': reverse('user-list')}]

    def get_success_url(self):
        return reverse('user-change', kwargs={'pk': self.object.pk})
