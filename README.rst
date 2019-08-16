django-cruditor
===============

.. image:: https://img.shields.io/pypi/v/django-cruditor.svg
   :target: https://pypi.python.org/pypi/django-cruditor
   :alt: Latest Version

.. image:: https://codecov.io/gh/moccu/django-cruditor/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/moccu/django-cruditor
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/django-cruditor/badge/?version=latest
   :target: https://django-cruditor.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/moccu/django-cruditor.svg?branch=master
   :target: https://travis-ci.org/moccu/django-cruditor

Usage
-----

Please refer to the `Documentation <https://django-cruditor.readthedocs.io/>`_ to
learn how to use ``django-cruditor``. Cruditor is a set of generic class based views
with UIKit styled templates. Together with django-tables2, django-filter and
django-tapeforms this package provides you some easy to use Django views to build
your customized CRUD interface.


Requirements
------------

django-cruditor supports Python 3 only and requires at least Django 1.11.
Optional dependencies are django-tapeforms, django-tables2 and django-filter.


Prepare for development
-----------------------

A Python 3.6 interpreter is required in addition to pipenv.

.. code-block:: shell

    $ pipenv install --python 3.6 --dev
    $ pipenv run pip install -e .


Now you can run the tests.

.. code-block:: shell

    $ pipenv run py.test


Now you're ready to start the example project to experiment with cruditor.

.. code-block:: shell

    $ pipenv run python examples/manage.py runserver
