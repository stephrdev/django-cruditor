from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.text import capfirst
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, DeleteView, FormView, TemplateView, UpdateView

from .forms import ChangePasswordForm
from .mixins import CruditorMixin, FormViewMixin


try:
    import django_tables2 as tables
except ImportError:
    # We don't want to break if django-tables2 is not available. Users would have
    # to overwrite the get_table method if they don't want to use django-tables2.
    tables = None


class Cruditor404View(CruditorMixin, TemplateView):
    """
    Customized not found page. Needed to add the required cruditor context
    for properly rendered templates.
    """

    #: Template used to render the 404 page.
    template_name = 'cruditor/404.html'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=404).render()


class Cruditor403View(CruditorMixin, TemplateView):
    """
    Customized permission denied page. Needed to add the required cruditor
    context for properly rendered templates.
    """

    #: Template used to render the 403 page.
    template_name = 'cruditor/403.html'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403).render()


class CruditorListView(CruditorMixin, TemplateView):
    """
    Enhanced list view backed by django-tables2 and django-filters.

    You want to set at least the ``model`` property. The remaining default
    property values are just fine for a working output.

    By providing a alternative ``table_class`` and/or ``filter_class`` you can
    improve the usability of the view even further.
    """

    #: Model to work on in this view.
    model = None

    #: Queryset to use for looking up objects.
    queryset = None

    #: Optional django_filters.FilterSet class to provide filtering capabilities.
    filter_class = None

    #: Required django_tables2.Table class to change the rendered table.
    table_class = None

    #: Template to use when rendering the list view.
    template_name = 'cruditor/list.html'

    def get_context_data(self, **kwargs):
        """
        Prepares the context by adding the ``table`` context variable.
        If you have configured ``filter_class``, the ``filter_form`` context
        variable will be provided too.
        """
        context = super().get_context_data(**kwargs)
        filtered_qs = self.get_filtered_queryset()
        context['table'] = self.get_table(filtered_qs)
        context['filter_form'] = filtered_qs.form if hasattr(filtered_qs, 'form') else None
        return context

    def get_queryset(self):
        """
        Provide a queryset to fetch data with. If ``queryset`` is set on the class,
        the value will be used, if not but ``model`` is set, the default manager
        is used.

        If both queryset and model is not set, you have to override this method
        to provide data to display.
        """
        if self.queryset is not None:
            return self.queryset

        if getattr(self, 'model', None):
            return self.model._default_manager.all()

        return []

    def get_table_class(self):
        """
        Method to override the used table class. By default, returns ``table_class``
        property if set.

        If no ``table_class``is provided, an ``ImproperlyConfigured`` exception is raised.
        """
        if not self.table_class:
            raise ImproperlyConfigured('table_class not configured.')
        return self.table_class

    def get_table_kwargs(self):
        """
        Override to provide additional kwargs when initializing the table object.
        """
        return {}

    def get_filter_class(self):
        """
        Method to override the used filter class from django_filters. By default,
        returns ``filter_class`` property if set.
        """
        return self.filter_class

    def get_filter_kwargs(self):
        """
        Override to provide additional kwargs when initializing the filterset object.
        """
        return {}

    def get_filtered_queryset(self):
        """
        Filter the base queryset using the django-filters FilterSet if available.
        QuerySet is passed if no ``filter_class`` is defined.
        """
        filter_class = self.get_filter_class()
        if filter_class:
            return filter_class(
                self.request.GET, queryset=self.get_queryset(), **self.get_filter_kwargs()
            )

        return self.get_queryset()

    def get_table(self, filtered_qs):
        """
        Prepare the table object using the provided QuerySet/Iterable.
        """
        qs = getattr(filtered_qs, 'qs', filtered_qs)
        if hasattr(qs, 'distinct'):
            qs = qs.distinct()
        table = self.get_table_class()(qs, **self.get_table_kwargs())
        tables.RequestConfig(self.request).configure(table)
        return table


class CruditorAddView(CruditorMixin, FormViewMixin, CreateView):
    """
    Enhanced view to add new items using a form view.
    """

    #: Message used when a new item was added successfully.
    success_message = _('The {model} "{object}" was successfully added.')

    #: Template used to render the add form view.
    template_name = 'cruditor/form.html'

    def get_object(self):
        """
        As we are in a add view, no object will be available ever.
        """
        return None

    def get_title(self):
        """
        Generate a sane title when adding new items using the
        ``get_model_verbose_name``.
        """
        return gettext('Add {0}').format(self.get_model_verbose_name())


class CruditorChangeView(CruditorMixin, FormViewMixin, UpdateView):
    """
    Enhanced view to edit existing items using a form view.
    """

    #: Message used when a item was changed successfully.
    success_message = _('The {model} "{object}" was successfully changed.')

    #: Template used to render the change form view.
    template_name = 'cruditor/form.html'

    def get_title(self):
        """
        Generate a sane title when editing an item using the __str__
        representation of a object.
        """
        return gettext('Change: {0}').format(self.object)

    def get_delete_url(self):
        """
        Override to provide a link for the delete button in the change view.
        By default no delete button is visible.
        """
        return None

    def get_context_data(self, **kwargs):
        """
        Add the ``object_delete_url`` context variable using ``get_delete_url``.
        Feel free to extend the context further.
        """
        return super().get_context_data(object_delete_url=self.get_delete_url(), **kwargs)


class CruditorDeleteView(CruditorMixin, DeleteView):
    """
    Enhanced view to delete existing items after a confirmation.
    """

    #: Message used when a item was deleted.
    success_message = _('The {model} "{object}" was successfully deleted.')

    #: Template used to render the confirmation form view.
    template_name = 'cruditor/delete.html'

    def delete(self, request, *args, **kwargs):
        """
        Call ``perform_delete`` method and redirect to the success URL with a
        nice success message. If there are protected related objects, an error
        message is shown instead with the output of ``format_linked_objects``.
        """
        self.object = self.get_object()
        try:
            self.perform_delete()
        except models.ProtectedError as e:
            return self.render_to_response(
                self.get_context_data(
                    linked_objects=self.format_linked_objects(e.protected_objects)
                )
            )
        messages.success(
            self.request,
            self.success_message.format(
                model=self.get_model_verbose_name(), object=self.object
            ),
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_title(self):
        """
        Generate a sane title when requesting a confirmation to delete an item
        using the __str__ representation of a object.
        """
        return gettext('Delete: {0}').format(self.object)

    def perform_delete(self):
        """
        Actual delete a object/model/item after confirmation.
        """
        self.object.delete()

    def format_linked_objects(self, objects):
        """
        Generate a list of strings describing the objects which have a protected
        relation to the item to delete.
        """
        return [
            gettext('{model}: {object}').format(
                model=capfirst(obj.__class__._meta.verbose_name), object=obj
            )
            for obj in objects
        ]


class CruditorChangePasswordView(CruditorMixin, FormView):
    """
    Enhanced view to perform password changes in the Cruditor context.
    """

    #: Template used when rendering the change password form.
    template_name = 'cruditor/form.html'

    #: Title for breadcrumb and page.
    title = _('Change password')

    #: Form used to change the password.
    form_class = ChangePasswordForm

    def get_form_kwargs(self):
        """
        The current user is passed to the provided ``form_class`` when initializing
        the change password form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Save the new password (by calling ``form.save``) and rotate the session
        authorization hash.
        """
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, gettext('Password changed successfully.'))
        return redirect(self.request.path)

    def get_context_data(self, **kwargs):
        """
        Set ``form_save_button_label`` context variable to change the button
        label for the change password form.
        """
        return super().get_context_data(
            form_save_button_label=gettext('Set new password'), **kwargs
        )


class CruditorLogoutView(CruditorMixin, LogoutView):
    """
    View to log out the current user. After logging out, a info is displayed.
    """

    #: Template used to display the info that the user was logged out.
    template_name = 'cruditor/logout.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            cruditor=self.get_cruditor_context(alternative_title='Logout'), **kwargs
        )
