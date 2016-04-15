import datetime
import importlib
import inspect
import os
import sys


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
sys.path.insert(0, os.path.abspath('..'))
import django
django.setup()

project = 'Django CRUDitor'
copyright = '{0:%Y}, Moccu GmbH & Co. KG'.format(datetime.date.today())

version = __import__('cruditor').__version__
release = version


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'sphinx.ext.linkcode',
]

intersphinx_mapping = {
    'python': ('http://docs.python.org/3.5', None),
    'django': (
        'https://docs.djangoproject.com/en/dev/',
        'https://docs.djangoproject.com/en/dev/_objects/'
    ),
}

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']
pygments_style = 'sphinx'


def linkcode_resolve(domain, info):
    """Link source code to GitHub."""
    github_user, project, head = 'moccu', 'django-cruditor', 'master'

    if domain != 'py' or not info['module']:
        return None

    filename = info['module'].replace('.', '/')
    module = importlib.import_module(info['module'])

    if os.path.splitext(module.__file__)[0].endswith('__init__'):
        filename += '/__init__'

    item = module
    lineno = ''

    for piece in info['fullname'].split('.'):
        item = getattr(item, piece)
        try:
            lineno = '#L%d' % inspect.getsourcelines(item)[1]
        except (TypeError, IOError):
            pass

    return ('https://github.com/{0}/{1}/blob/{2}/{3}.py{4}'.format(
        github_user, project, head, filename, lineno))


def skip(app, what, name, obj, skip, options):
    if name == "__init__" and obj.__doc__:
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

if os.environ.get('READTHEDOCS', None) == 'True':
    html_theme = 'sphinx_rtd_theme'
else:
    html_theme = 'default'
