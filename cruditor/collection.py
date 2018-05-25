import django_tables2 as tables
from django.urls import reverse
from django.utils.translation import ugettext

from .views import CruditorAddView, CruditorChangeView, CruditorDeleteView, CruditorListView


class CollectionViewMixin(object):
    """
    Mixin to provide some extra default functionality to Cruditor views to make
    building views for a collection of data (like a Django model) even easier.
    """

    #: Title for collection list view
    collection_list_title = 'Collection'
    #: URL name to use when linking to the list view (e.g. in breadcrumb)
    collection_list_urlname = None
    #: URL name when linking to a detail page of a item (e.g. in list table or breadcrumb)
    collection_detail_urlname = None

    def get_title(self):
        """
        The method returns the ``collection_list_title`` when the view is a list view.
        All other views rely on the default behavior of cruditor.
        """
        if issubclass(self.__class__, CruditorListView):
            return self.collection_list_title
        return super().get_title()

    def get_breadcrumb_title(self):
        """
        The breadcrumb title returns "Delete" for delete views, default breadcrumb
        for all other views.
        """
        if issubclass(self.__class__, CruditorDeleteView):
            return ugettext('Delete')
        return super().get_breadcrumb_title()

    def get_breadcrumb(self):
        """
        This method creates the required breadcrumb items for the collection following
        some rules:

            * No extra items for list view
            * list view element when the ``collection_include_list_crumb`` method is true.
            * detail view element when the ``collection_include_detail_crumb`` method is true.
        """
        breadcrumb = super().get_breadcrumb()

        if self.collection_include_list_crumb():
            breadcrumb.append({
                'title': self.get_collection_list_title(),
                'url': self.get_collection_list_url(),
            })

        if self.collection_include_detail_crumb():
            breadcrumb.append({
                'title': self.get_collection_detail_title(),
                'url': self.get_collection_detail_url(),
            })

        return breadcrumb

    def get_table_class(self):
        """
        This method returns the django-tables2 Table class to use in the list view.
        If no class is defined, a new Table class is created (with one linked column).
        """
        if self.table_class:
            return self.table_class

        if not hasattr(self, '_table_class'):
            class CollectionTable(tables.Table):
                item = tables.LinkColumn(
                    self.collection_detail_urlname,
                    args=(tables.A('pk'),),
                    verbose_name=self.get_model_verbose_name(),
                    text=lambda obj: str(obj),
                    accessor=tables.A('pk')
                )

            self._table_class = CollectionTable

        return self._table_class

    def collection_include_list_crumb(self):
        """
        If this method returns true, the list view should be included in the breadcrumb.
        """
        return not issubclass(self.__class__, CruditorListView)

    def collection_include_detail_crumb(self):
        """
        If this method returns true, the detail view should be included in the breadcrumb.
        """
        return (
            self.collection_include_list_crumb() and
            hasattr(self, 'object') and
            not issubclass(self.__class__, (CruditorAddView, CruditorChangeView))
        )

    def get_collection_list_title(self):
        """
        Helper method to override the used collection list title.
        By default, just returns the class property.
        """
        return self.collection_list_title

    def get_collection_list_url(self):
        """
        Helper method to generate the collection list url.
        By default, just calls reverse with the ``collection_list_urlname`` property.
        """
        return reverse(self.collection_list_urlname)

    def get_collection_detail_title(self):
        """
        Helper method to override the used collection detail title.
        By default, just returns the str-representation of the requested item.
        """
        return str(self.object)

    def get_collection_detail_url(self):
        """
        Helper method to generate the collection detail url for the current object.
        By default, calls reverse with the ``collection_detail_urlname`` property
        and passes the object pk to the function call.
        """
        return reverse(self.collection_detail_urlname, args=(self.object.pk,))
