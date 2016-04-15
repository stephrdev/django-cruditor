import codecs
import os
import sys

from setuptools import setup, find_packages


VERSION = __import__('cruditor').__version__


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (VERSION, VERSION))
    print('  git push --tags')
    sys.exit()


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


# TEMPORARY FIX FOR
# https://bitbucket.org/pypa/setuptools/issues/450/egg_info-command-is-very-slow-if-there-are
TO_OMIT = ['.git', '.tox']
orig_os_walk = os.walk
def patched_os_walk(path, *args, **kwargs):
    for (dirpath, dirnames, filenames) in orig_os_walk(path, *args, **kwargs):
        if '.git' in dirnames:
            # We're probably in our own root directory.
            print("MONKEY PATCH: omitting a few directories like .git and .tox...")
            dirnames[:] = list(set(dirnames) - set(TO_OMIT))
        yield (dirpath, dirnames, filenames)

os.walk = patched_os_walk
# END IF TEMPORARY FIX.


test_requirements = [
    'tox',
    'tox-pyenv',
    'mock',
    'factory-boy',
    'pydocstyle',
    'pytest',
    'pytest-cov',
    'pytest-flakes',
    'pytest-pep8',
    'pytest-django',
    'pytest-isort',
]


setup(
    name='django-cruditor',
    version=VERSION,
    url='https://github.com/moccu/django-cruditor',
    author='Moccu GmbH & Co. KG',
    author_email='info@moccu.com',
    description='Set of generic class based views with Bootstrap templates.',
    long_description=read('README.rst'),
    license='BSD',
    packages=find_packages(exclude=['examples*', 'tests*']),
    include_package_data=True,
    install_requires=[
        'django>=1.8,<1.10',
        'django-floppyforms>=1.6,<1.7',
        'django-filter>=0.13,<0.14',
        'django-tables2>=1.1,<1.2',
    ],
    extras_require={
        'tests': test_requirements,
        'docs': ['sphinx>=1.4,<1.5'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
