Installation
============

django-cruditor supports Python 3 only and requires at least Django 4.2 and
django-tapeforms. Optional dependencies are django-tables2 and django-filter.
Depending on what parts of django-cruditor you want to use, you have to install
them manually.

To start, simply install the latest stable package using the command

.. code-block:: shell

    $ pip install django-cruditor


In addition, you have to add ``'cruditor'`` and ``tapeforms`` to the ``INSTALLED_APPS``
setting in your ``settings.py``.

If you're planing to us the ListViews provided django-cruditor, you have to install
``django-tables2`` and add need to add ``'django_tables2'`` to your ``INSTALLED_APPS``.

Finally, if you want to use the filtering capabilities of django-cruditor ListViews,
install ``django-filter`` and add ``django_filters`` to your ``INSTALLED_APPS``.

Thats it, now continue to the :doc:`Usage section <usage>` to learn how to render your
forms to HTML.
