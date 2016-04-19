django-cruditor
===============

.. image:: https://badge.fury.io/py/django-cruditor.png
    :target: http://badge.fury.io/py/django-cruditor

.. image:: https://travis-ci.org/moccu/django-cruditor.svg?branch=master
    :target: https://travis-ci.org/moccu/django-cruditor

.. image:: https://coveralls.io/repos/moccu/django-cruditor/badge.svg
    :target: https://coveralls.io/r/moccu/django-cruditor

.. image:: https://readthedocs.org/projects/django-cruditor/badge/?version=latest
    :target: https://readthedocs.org/projects/django-cruditor/?badge=latest


What is django-cruditor
-----------------------

`django-cruditor` is a set of generic class based views with Bootstrap templates.
Together with `django-tables2`, `django-filter` and `django-floppyforms` this
module provides you some easy to use Django views to build your customized
CRUD interface.


Quick start
-----------

To install `django-cruditor` just use your preferred Python package installer::

    $ pip install django-cruditor

Add the `django-cruditor` and its dependencies to to your Django settings

.. code-block:: python

    INSTALLED_APPS = (
        # some other apps
        'floppyforms',
        'django_tables2',
        'cruditor',
    )

Please refer to the examples to see how it works. More documentation will be
added soon.


Contribute
----------

To contribute, you can use `pip install -e .[tests]` to install all required
development packages. To run the tests, just use

.. code-block:: shell

    $ tox

If you don't know where to start, have a look at the `TODO` file in this
repository.
