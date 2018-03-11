Installation
============

django-cruditor supports Python 3 only and requires at least Django 1.11 (because
of the template based widget rendering). Optional dependencies are django-tables2,
django-filter and django-tapeforms. Depending on what parts of django-cruditor you
want to use, you have to install them manually.

To start, simply install the latest stable package using the command

.. code-block:: shell

    $ pip install django-cruditor


In addition, you have to add ``'cruditor'`` to the ``INSTALLED_APPS`` setting
in your ``settings.py``.

If you're planing to us the ListViews provided django-cruditor, you have to install
``django-tables2`` and add need to add ``'django_tables2'`` to your ``INSTALLED_APPS``.

If you want to use the form rendering of the Add- or ChangeViews, you'll need
``django-tapeforms``. Don't forget to add ``tapeforms`` to your settings'
``INSTALLED_APPS``.

Finally, if you want to use the filtering capabilities of django-cruditor ListViews,
install ``django-filter`` and add ``django_filters`` to your ``INSTALLED_APPS``.

Thats it, now continue to the :doc:`Usage section <usage>` to learn how to render your
forms to HTML.
