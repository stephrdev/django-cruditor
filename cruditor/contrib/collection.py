from django.urls import reverse
from django.utils.translation import ugettext

from ..views import CruditorAddView, CruditorChangeView, CruditorDeleteView, CruditorListView


class CollectionViewMixin(object):
    collection_list_title = 'Collection'
    collection_list_urlname = None
    collection_detail_urlname = None

    def get_title(self):
        if issubclass(self.__class__, CruditorChangeView):
            return ugettext('Change: {0}').format(self.object)
        elif issubclass(self.__class__, CruditorDeleteView):
            return ugettext('Delete: {0}').format(self.object)
        elif issubclass(self.__class__, CruditorAddView):
            return ugettext('Add {0}').format(self.model._meta.verbose_name)
        else:
            return super().get_title()

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

    def collection_include_list_crumb(self):
        return not issubclass(self.__class__, CruditorListView)

    def collection_include_detail_crumb(self):
        return (
            self.include_list_crumb() and
            not issubclass(self.__class__, (CruditorAddView, CruditorChangeView))
        )

    def get_collection_list_title(self):
        return self.collection_list_title

    def get_collection_list_url(self):
        return reverse(self.collection_list_urlname)

    def get_collection_detail_title(self):
        return self.object.name

    def get_collection_detail_url(self):
        return reverse(self.collection_detail_urlname, args=(self.object.pk,))
