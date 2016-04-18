import django_tables2 as tables
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import logout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, FormView, TemplateView, UpdateView, View
from django.views.generic.detail import SingleObjectMixin

from .forms import ChangePasswordForm, DeleteConfirmForm
from .mixins import CruditorMixin, FormsetViewMixin


class Cruditor404View(CruditorMixin, TemplateView):
    template_name = 'cruditor/404.html'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=404).render()


class Cruditor403View(CruditorMixin, TemplateView):
    template_name = 'cruditor/403.html'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403).render()


class CruditorListView(CruditorMixin, TemplateView):
    model = None
    queryset = None
    filter_class = None
    table_class = tables.Table
    template_name = 'cruditor/list.html'

    def get_context_data(self, **kwargs):
        context = super(CruditorListView, self).get_context_data(**kwargs)
        filtered_qs = self.get_filtered_queryset()
        context['table'] = self.get_table(filtered_qs)
        context['filter_form'] = filtered_qs.form if self.filter_class else None

        return context

    def get_queryset(self):
        return self.queryset or self.model._default_manager.all()

    def get_table_class(self):
        return self.table_class

    def get_table_kwargs(self):
        return {}

    def get_filter_class(self):
        return self.filter_class

    def get_filter_kwargs(self):
        return {}

    def get_filtered_queryset(self):
        if self.filter_class:
            return self.get_filter_class()(
                self.request.GET,
                queryset=self.get_queryset(),
                **self.get_filter_kwargs()
            )

        return self.get_queryset()

    def get_table(self, filtered_qs):
        qs = getattr(filtered_qs, 'qs', filtered_qs).distinct()
        table = self.get_table_class()(qs, **self.get_table_kwargs())
        tables.RequestConfig(self.request).configure(table)
        return table


class CruditorAddView(CruditorMixin, FormsetViewMixin, CreateView):
    success_message = _('The {model} "{object}" was successfully added.')
    template_name = 'cruditor/form.html'

    def get_object(self):
        return None

    def get_title(self):
        return ugettext('Add {0}').format(self.model._meta.verbose_name)


class CruditorChangeView(CruditorMixin, FormsetViewMixin, UpdateView):
    success_message = _('The {model} "{object}" was successfully changed.')
    template_name = 'cruditor/form.html'

    def get_title(self):
        return ugettext('Change: {0}').format(self.object)

    def get_delete_url(self):
        return None

    def get_context_data(self, **kwargs):
        return super(CruditorChangeView, self).get_context_data(
            object_delete_url=self.get_delete_url(), **kwargs)


class CruditorDeleteView(CruditorMixin, SingleObjectMixin, FormView):
    success_message = _('The {model} "{object}" was successfully deleted.')
    template_name = 'cruditor/delete.html'
    form_class = DeleteConfirmForm

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CruditorDeleteView, self).dispatch(request, *args, **kwargs)

    def get_title(self):
        return ugettext('Delete: {0}').format(self.object)

    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, self.success_message.format(
            model=self.model._meta.verbose_name, object=self.object))
        return super(CruditorDeleteView, self).form_valid(form)


class CruditorChangePasswordView(CruditorMixin, FormView):
    template_name = 'cruditor/change-password.html'
    title = _('Change password')
    form_class = ChangePasswordForm

    def get_form_kwargs(self):
        kwargs = super(CruditorChangePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, ugettext('Password changed successfully.'))
        return redirect(self.request.path)


class CruditorLogoutView(CruditorMixin, View):
    template_name = 'cruditor/logout.html'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return logout(
            request,
            template_name=self.template_name,
            extra_context={
                'cruditor': self.get_cruditor_context(alternative_title='Logout')
            },
        )
