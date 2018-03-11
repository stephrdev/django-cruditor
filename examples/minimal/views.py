from cruditor.mixins import CruditorMixin
from django.views.generic import TemplateView

from examples.mixins import ExamplesMixin


class DemoView(ExamplesMixin, CruditorMixin, TemplateView):
    title = 'Demo view'
    template_name = 'minimal/demo.html'
