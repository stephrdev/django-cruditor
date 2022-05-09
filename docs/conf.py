import datetime
import importlib
import inspect
import sys

import os

year = datetime.datetime.now().strftime("%Y")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
import django
django.setup()

sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'sphinx.ext.linkcode',
]


def linkcode_resolve(domain, info):
    """Link source code to GitHub."""
    project = 'django-cruditor'
    github_user = 'stephrdev'
    head = 'master'

    if domain != 'py' or not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    mod = importlib.import_module(info['module'])
    basename = os.path.splitext(mod.__file__)[0]
    if basename.endswith('__init__'):
        filename += '/__init__'
    item = mod
    lineno = ''
    for piece in info['fullname'].split('.'):
        item = getattr(item, piece)
        try:
            lineno = '#L%d' % inspect.getsourcelines(item)[1]
        except (TypeError, IOError):
            pass
    return ("https://github.com/%s/%s/blob/%s/%s.py%s" %
            (github_user, project, head, filename, lineno))


intersphinx_mapping = {
    'python': ('http://docs.python.org/3.6', None),
    'django': ('https://docs.djangoproject.com/en/dev/',
               'https://docs.djangoproject.com/en/dev/_objects/'),
}

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'django-cruditor'
copyright = '%s, Stephan Jaekel' % year

exclude_patterns = ['_build']

pygments_style = 'sphinx'


def skip(app, what, name, obj, skip, options):
    if name == '__init__' and obj.__doc__:
        return False
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip)


autodoc_default_flags = ['members', 'show-inheritance']
autodoc_member_order = 'bysource'

inheritance_graph_attrs = dict(rankdir='TB')

inheritance_node_attrs = dict(shape='rect', fontsize=14, fillcolor='gray90',
                              color='gray30', style='filled')

inheritance_edge_attrs = dict(penwidth=0.75)

html_theme = 'default'
