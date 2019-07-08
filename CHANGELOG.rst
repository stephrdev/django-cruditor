Changelog
=========

1.3.0 - 2019-07-08
------------------

* Catch the exception and show an error message when deleting an item with
  protected related objects
* Remove ``DeleteConfirmForm`` to replace the checkbox by a simple message and
  make the deletion process lighter


1.2.1 - 2019-03-26
------------------

* Fix a bug when a user is not logged in but get_titlebuttons/get_breadcrumb
  relies on self.object


1.2.0 - 2019-03-18
------------------

* Add French translations
* Improve templates for tables
* Fix packaging bug when installed as git checkout
* Fix filter_class related bug in list views


1.1.1 - 2018-08-27
------------------

* Remove local style fix for invalid form inputs, fixed in upstream django-tapeforms


1.1.0 - 2018-08-17
------------------

* Add support for Django 2.1
* Use auth class based views for login an logout instead of function based views.


1.0.0 - 2018-05-25
------------------

* Many bugfixes and small improvements
* Add CollectionMixin
* Add ``get_titlebuttons`` helper to add additional buttons to Cruditor views
* Refactor templates to use UIKit instead of Bootstrap 3
* Introduce build process for Javascript and CSS files
* Add support for formsets, including Javascript for the user interface


0.1.4
-----

* Update translations.


0.1.3
-----

* Add missing floppyforms load tag.


0.1.2
-----

* Add floppyforms form tag to inline formset template.


0.1.1
-----

* Added some useful template blocks.


0.1.0
-----

* Initial release without many docs but an example project.
