from django.views.generic import TemplateView

from cruditor.mixins import CruditorMixin
from examples.mixins import ExamplesMixin
from cruditor.datastructures import Breadcrumb


class DemoView(ExamplesMixin, CruditorMixin, TemplateView):
    title = 'Demo view'
    template_name = 'minimal/demo.html'

    def get_breadcrumb(self):
        return super().get_breadcrumb() + [
            Breadcrumb(url='/', title='Additional breadcrumb'),
            Breadcrumb(title='Disabled item'),
        ]
