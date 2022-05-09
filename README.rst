django-cruditor
===============

.. image:: https://img.shields.io/pypi/v/django-cruditor.svg
   :target: https://pypi.org/project/django-cruditor/
   :alt: Latest Version

.. image:: https://github.com/stephrdev/django-cruditor/workflows/Test/badge.svg?branch=master
   :target: https://github.com/stephrdev/django-cruditor/actions?workflow=Test
   :alt: CI Status

.. image:: https://codecov.io/gh/stephrdev/django-cruditor/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/stephrdev/django-cruditor
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/django-cruditor/badge/?version=latest
   :target: https://django-cruditor.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status


Usage
-----

Please refer to the `Documentation <https://django-cruditor.readthedocs.io/>`_ to
learn how to use ``django-cruditor``. Cruditor is a set of generic class based views
with UIKit styled templates. Together with django-tables2, django-filter and
django-tapeforms this package provides you some easy to use Django views to build
your customized CRUD interface.


Requirements
------------

django-cruditor supports Python 3 only and requires at least Django 2.2.
Optional dependencies are django-tapeforms, django-tables2 and django-filter.


Prepare for development
-----------------------

A Python 3 interpreter is required in addition to poetry.

.. code-block:: shell

    $ poetry install
    # If you want to build docs, execute this in addition
    $ poetry install -E docs


Now you're ready to start the example project to experiment with cruditor.

.. code-block:: shell

    $ poetry run python examples/manage.py runserver
