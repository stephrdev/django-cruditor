import django_tables2 as tables
from django.urls import reverse
from django.utils.translation import ugettext

from ..views import CruditorAddView, CruditorChangeView, CruditorDeleteView, CruditorListView


class CollectionViewMixin(object):
    collection_list_title = 'Collection'
    collection_list_urlname = None
    collection_detail_urlname = None

    def get_title(self):
        if issubclass(self.__class__, CruditorListView):
            return self.collection_list_title
        return super().get_title()

    def get_breadcrumb_title(self):
        if issubclass(self.__class__, CruditorDeleteView):
            return ugettext('Delete')
        return super().get_breadcrumb_title()

    def get_breadcrumb(self):
        breadcrumb = super().get_breadcrumb()

        if not hasattr(self, 'object'):
            return breadcrumb

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
        return not issubclass(self.__class__, CruditorListView)

    def collection_include_detail_crumb(self):
        return (
            self.collection_include_list_crumb() and
            not issubclass(self.__class__, (CruditorAddView, CruditorChangeView))
        )

    def get_collection_list_title(self):
        return self.collection_list_title

    def get_collection_list_url(self):
        return reverse(self.collection_list_urlname)

    def get_collection_detail_title(self):
        return str(self.object)

    def get_collection_detail_url(self):
        return reverse(self.collection_detail_urlname, args=(self.object.pk,))
