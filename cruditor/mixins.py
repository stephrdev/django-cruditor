from django.contrib import messages
from django.contrib.auth.views import REDIRECT_FIELD_NAME, login
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .forms import LoginForm


class CruditorMixin(object):
    menu_title = 'CRUDitor'
    index_url = '#'
    logout_url = '#'
    change_password_url = None
    menu_template_name = 'cruditor/includes/menu.html'
    extrahead_template_name = 'cruditor/includes/extrahead.html'
    login_template_name = 'cruditor/login.html'
    staff_required = True
    required_permission = None

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_active or (self.staff_required and not request.user.is_staff):
            login_defaults = {
                'template_name': self.login_template_name,
                'authentication_form': LoginForm,
                'extra_context': {
                    'app_path': request.get_full_path(),
                    'next_field': REDIRECT_FIELD_NAME,
                    'next_value': request.get_full_path(),
                    'cruditor': self.get_cruditor_context(alternative_title='Login'),
                },
            }
            return login(request, **login_defaults)

        self.ensure_required_permission()

        return super(CruditorMixin, self).dispatch(request, *args, **kwargs)

    def get_cruditor_context(self, alternative_title=None):
        return {
            'title': alternative_title or self.get_title(),
            'breadcrumb': self.get_breadcrumb() + [
                {'title': alternative_title or self.get_breadcrumb_title(), 'url': None}
            ],
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
        return getattr(self, 'title', self.menu_title)

    def get_breadcrumb_title(self):
        return self.get_title()

    def get_breadcrumb(self):
        return []

    def get_required_permission(self):
        return self.required_permission

    def ensure_required_permission(self):
        required_permission = self.get_required_permission()

        if not required_permission:
            return

        if not self.request.user.has_perm(required_permission):
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(CruditorMixin, self).get_context_data(**kwargs)
        context['cruditor'] = self.get_cruditor_context()
        return context


class FormsetViewMixin(object):
    formset_classes = None

    def get_formset_classes(self):
        return self.formset_classes or {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return self.render_to_response(self.get_context_data(
            form=self.get_form(self.get_form_class()),
            **dict([(
                formset_name,
                formset_class(instance=self.object)
            ) for formset_name, formset_class in self.get_formset_classes().items()])
        ))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form(self.get_form_class())
        formsets = dict([(
            formset_name,
            formset_class(request.POST, files=request.FILES, instance=self.object)
        ) for formset_name, formset_class in self.get_formset_classes().items()])

        if all([form.is_valid()] + [formset.is_valid() for formset in formsets.values()]):
            return self.form_valid(form, **formsets)
        else:
            return self.form_invalid(form, **formsets)

    def form_valid(self, form, **formsets):
        self.object = form.save()

        self.formset_objects = {}
        for formset_name, formset in formsets.items():
            formset.instance = self.object
            self.formset_objects[formset_name] = formset.save()

        messages.success(self.request, self.success_message.format(
            model=self.model._meta.verbose_name, object=self.object))

        return redirect(self.get_success_url())

    def form_invalid(self, form, **formsets):
        return self.render_to_response(self.get_context_data(
            form=form,
            formset_errors=True,
            **formsets
        ))
