from django.views.generic import TemplateView

from cruditor.mixins import CruditorMixin
from examples.mixins import ExamplesMixin


class DemoView(ExamplesMixin, CruditorMixin, TemplateView):
    title = 'Demo view'
    template_name = 'minimal/demo.html'

    def get_breadcrumb(self):
        return super().get_breadcrumb() + [
            {
                'url': '/',
                'title': 'Additional breadcrumb',
            },
            {
                'title': 'Disabled item',
            },
        ]
