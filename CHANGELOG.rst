Changelog
=========

2.3.2 - 2022-09-08
------------------

* Expose newForm in formset add callback.
* Add more template blocks for formset template.


2.3.1 - 2022-08-04
------------------

* Fix issue with logout view


2.3.0 - 2022-08-03
------------------

* Fix issue with small buttons
* Fix spacing issue with title buttons
* Add support for target in title buttons.


2.2.0 - 2022-08-02
------------------

* Ship scss and js files with source distribution
* Add extra blocks for title section for better customization


2.1.0 - 2022-06-23
------------------

* Add get_formset_kwargs method to FormViewMixin


2.0.0 - 2022-05-09
------------------

* Drop support for Django < 2.2
* Add template_context property for formsets


1.4.0 - 2019-09-26
------------------

* Add method to customize the success message of change form views


1.3.2 - 2019-08-16
------------------

* Improve formset js component


1.3.1 - 2019-08-16
------------------

* Fix issue with formsets and duplicated DELETE inputs
* Fix broken delete callback in formset js module


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
