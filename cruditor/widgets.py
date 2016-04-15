import floppyforms.__future__ as forms


class CruditorSplitDateTimeWidget(forms.SplitDateTimeWidget):
    def __init__(self, *args, **kwargs):
        super(CruditorSplitDateTimeWidget, self).__init__(*args, **kwargs)
        self.widgets[0].template_name = 'cruditor/forms/input.html'
        self.widgets[1].template_name = 'cruditor/forms/input.html'

    def format_output(self, rendered_widgets):
        return (
            '<div class="row">'
            '<div class="col-xs-6">{0}</div>'
            '<div class="col-xs-6">{1}</div>'
            '</div>'
        ).format(*rendered_widgets)


class CruditorAutoSlugWidget(forms.TextInput):
    autoslug = None

    def __init__(self, autoslug, css_class='slugify', *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({'data-autoslug': autoslug, 'class': css_class})
        super(CruditorAutoSlugWidget, self).__init__(*args, **kwargs)

    class Media:
        js = (
            'cruditor/js/jquery-slugify/jquery.slugify.js',
            'cruditor/js/jquery-slugify/slugify-activator.js',
        )


class CruditorSelectMultiple(forms.widgets.SelectMultiple):

    def __init__(self, css_class='select2-multiple', *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({'class': css_class})
        super(CruditorSelectMultiple, self).__init__(*args, **kwargs)

    class Media:
        css = {
            'all': (
                'cruditor/css/select2.css',
                'cruditor/css/bootstrap-select2.css'
            )
        }
        js = (
            'cruditor/js/bootstrap-select2/select2.js',
            'cruditor/js/bootstrap-select2/select2-activator.js',
        )
