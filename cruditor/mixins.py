from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.views import REDIRECT_FIELD_NAME, login
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .forms import LoginForm


class CruditorMixin(object):
    """
    Base mixin for all Cruditor views. Provides common functionality for all views.

    It is a good idea to have a own "base" mixin to configure the common options
    like ``menu_title``, the urls and templates.

    Usually you might have ``required_permission`` configured per-view.
    """

    #: Title to use in templates / menu bar
    menu_title = 'CRUDitor'

    #: URL to use in the linked menu_title
    index_url = '#'

    #: URL to use when providing a logout link to the user.
    logout_url = '#'

    #: URL to the change password view, if available.
    change_password_url = None

    #: Template name which is included to render the menu.
    menu_template_name = 'cruditor/includes/menu.html'

    #: Template used to include extra head stuff.
    extrahead_template_name = 'cruditor/includes/extrahead.html'

    #: Page template for the login view.
    login_template_name = 'cruditor/login.html'

    #: Form class which is used in the login view.
    login_form_class = LoginForm

    #: Decide if only staff users should be able to use the Cruditor views.
    staff_required = True

    #: Which permission is required to access the view.
    required_permission = None

    #: If not provided, Cruditor tries to look up the verbose name from ``model.Meta``
    model_verbose_name = None

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        """
        Ensure the user is logged in (by calling `ensure_logged_in`` method).
        If the user is logged in, permissions are checked by calling
        ``ensure_required_permission``.
        """
        login_result = self.ensure_logged_in(request, *args, **kwargs)
        if login_result is not True:
            return login_result

        self.ensure_required_permission()

        return super().dispatch(request, *args, **kwargs)

    def get_cruditor_context(self, alternative_title=None):
        """
        Provides some context for all Cruditor templates to render menu, header,
        breadcrumb and title buttons.

        The method takes an optional argument ``alternative_title`` to override
        the default title from ``get_title`` method.
        """
        return {
            'title': alternative_title or self.get_title(),
            'breadcrumb': self.get_breadcrumb() + [
                {'title': alternative_title or self.get_breadcrumb_title(), 'url': None}
            ],
            'titlebuttons': self.get_titlebuttons(),
            'constants': {
                'menu_title': self.menu_title,
                'menu_template_name': self.menu_template_name,
                'extrahead_template_name': self.extrahead_template_name,
                'index_url': self.index_url,
                'logout_url': self.logout_url,
                'change_password_url': self.change_password_url,
            }
        }

    def get_title(self):
        """
        Returns the title of the page. Uses view's ``title`` property. If not set
        falls back to ``menu_title``.
        """
        return getattr(self, 'title', self.menu_title)

    def get_breadcrumb_title(self):
        """
        By default, the breadcrumb title is the same as the page title.
        Calls ``get_title`` if not overwritten.
        """
        return self.get_title()

    def get_breadcrumb(self):
        """
        This method is expected to return a list of breadcrumb elements as a list.

        Every breadcrumb element is a dict or object with at least
        a ``title`` property/key. If a ``url`` key/property is provided, the item
        is linked.
        """
        return []

    def get_titlebuttons(self):
        """
        This method is expected to return None or a list of buttons to display in
        the title row of the page.

        Every button element is a dict or object with at least a ``label`` and
        ``url`` property/key. In addition, one can provide an alternative
        ``button_class`` which is used as a css class - pefixed with "btn-".
        Default ``button_class`` is "light".
        """
        return None

    def get_model_verbose_name(self):
        """
        Returns the verbose name of the handled object/item.

        If ``model_verbose_name`` is set, the value is used. If not, Cruditor
        tries to get the verbose name from the model property (via Meta class).
        If no name is available at all, "Item" is returned.
        """
        if self.model_verbose_name:
            return self.model_verbose_name
        if getattr(self, 'model', None):
            return self.model._meta.verbose_name
        return 'Item'

    def ensure_logged_in(self, request, *args, **kwargs):
        """
        This method checks if the request user is logged in and has the right
        flags set (e.g. ``is_staff`` if ``staff_required`` is set in view).

        If user is logged in, ``True`` is returned.
        If not, ``handle_not_logged_in`` is called.
        """
        if (
            not request.user.is_active or
            (self.staff_required and not request.user.is_staff)
        ):
            return self.handle_not_logged_in(request, *args, **kwargs)

        return True

    def handle_not_logged_in(self, request, *args, **kwargs):
        """
        This method is responsible to handle not logged-in users.
        By default, renders the Django login view using a Cruditor optimized
        template using the ``login_form_class`` as Form.
        """
        login_defaults = {
            'template_name': self.login_template_name,
            'authentication_form': self.login_form_class,
            'extra_context': {
                'app_path': request.get_full_path(),
                'next_field': REDIRECT_FIELD_NAME,
                'next_value': request.get_full_path(),
                'cruditor': self.get_cruditor_context(alternative_title='Login'),
            },
        }
        return login(request, **login_defaults)

    def get_required_permission(self):
        """
        Returns the required Django permissions required to access the view.

        You might override the method to apply more complex rules on what
        permissions are required.
        """
        return self.required_permission

    def ensure_required_permission(self):
        """
        This method ensures that all required permissions (fetched by calling
        ``get_required_permission``).

        If permissions are not met, ``PermissionDenied`` is raised.
        """
        required_permission = self.get_required_permission()

        if not required_permission:
            return

        if not self.request.user.has_perm(required_permission):
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        """
        Adds the ``cruditor`` context variable to the template context. Uses data
        from ``get_cruditor_context`` method.
        """
        context = super().get_context_data(**kwargs)
        context['cruditor'] = self.get_cruditor_context()
        return context


class FormViewMixin(object):
    """
    Mixin to add formset support to Django FormViews. To use formsets,
    you have to provide a set of formsets as a dict (or OrderedDict if you have
    more than one formset - just to have a defined ordering).
    """
    formset_classes = None

    def get_formset_classes(self):
        """
        This method returns the formset classes to render in the form view.
        By default, returns the ``formset_classes`` property.
        """
        return self.formset_classes or {}

    def get(self, request, *args, **kwargs):
        """
        Extended get-method to render to form and all formsets properly initialized.
        """
        self.object = self.get_object()

        formsets = OrderedDict([(
            formset_name,
            formset_class(instance=self.object)
        ) for formset_name, formset_class in self.get_formset_classes().items()])

        return self.render_to_response(self.get_context_data(
            form=self.get_form(self.get_form_class()),
            formsets=formsets,
        ))

    def post(self, request, *args, **kwargs):
        """
        Extended version of the FormView.post method which validates the form and
        all configured formsets. If everything is valid, ``form_valid`` is called.
        If something is not valid, ``form_invalid`` is called.

        Both the form instance and all formset instances are provided to the called
        method. The form is passed as the first argument, the formsets are passed
        as keyword arguments using the formset key from ``formset_classes``.
        """
        self.object = self.get_object()

        form = self.get_form(self.get_form_class())
        formsets = OrderedDict([(
            formset_name,
            formset_class(request.POST, files=request.FILES, instance=self.object)
        ) for formset_name, formset_class in self.get_formset_classes().items()])

        if all([form.is_valid()] + [formset.is_valid() for formset in formsets.values()]):
            return self.form_valid(form, **formsets)
        else:
            return self.form_invalid(form, **formsets)

    def save_form(self, form, **formsets):
        """
        This method is called from ``form_valid`` to actual save the data from the
        form and all formsets. All saving is done by default.
        """
        self.object = form.save()

        self.formset_objects = {}
        for formset_name, formset in formsets.items():
            formset.instance = self.object
            self.formset_objects[formset_name] = formset.save()

    def form_valid(self, form, **formsets):
        """
        Saves the data and provides a nice success message, then redirects to the
        ``get_success_url`` url.
        """
        self.save_form(form, **formsets)

        messages.success(self.request, self.success_message.format(
            model=self.get_model_verbose_name(), object=self.object))

        return redirect(self.get_success_url())

    def form_invalid(self, form, **formsets):
        """
        Re-render the page with the invalid form and/or formsets.
        """
        return self.render_to_response(self.get_context_data(
            form=form,
            formsets=formsets,
            formset_errors=True,
        ))
