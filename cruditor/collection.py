import django_tables2 as tables
from django.conf import settings
from django.urls import path, reverse
from django.utils.translation import gettext

from cruditor.datastructures import Breadcrumb, TitleButton
from cruditor.views import (
    CruditorAddView,
    CruditorChangeView,
    CruditorDeleteView,
    CruditorListView,
)


class CollectionViewMixin:
    """
    Mixin to provide some extra default functionality to Cruditor views to make
    building views for a collection of data (like a Django model) even easier.
    """

    #: Title for collection list view
    collection_list_title = "Collection"
    #: URL name to use when linking to the list view (e.g. in breadcrumb)
    collection_list_urlname = None
    #: URL name to use when linking to the add view (e.g. in title buttons)
    collection_add_urlname = None
    #: URL name when linking to a detail page of a item (e.g. in list table or breadcrumb)
    collection_detail_urlname = None
    #: URL name when linking to the delete page of a item (e.g. in change view)
    collection_delete_urlname = None

    def get_title(self):
        """
        The method calls the ``get_collection_list_title`` method when the view is a list view.
        All other views rely on the default behavior of cruditor.
        """
        if issubclass(self.__class__, CruditorListView):
            return self.get_collection_list_title()
        return super().get_title()

    def get_success_url(self):
        if (
            issubclass(self.__class__, (CruditorAddView, CruditorChangeView))
            and self.collection_detail_urlname
        ):
            return self.get_collection_object_success_url()

        if issubclass(self.__class__, CruditorDeleteView) and self.collection_list_urlname:
            return self.get_collection_list_url()

        return super().get_success_url()

    def get_delete_url(self):
        if self.collection_delete_urlname:
            return self.get_collection_delete_url()
        return None

    def get_breadcrumb_title(self):
        """
        The breadcrumb title returns "Delete" for delete views, default breadcrumb
        for all other views.
        """
        if issubclass(self.__class__, CruditorDeleteView):
            return gettext("Delete")
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
            breadcrumb.append(
                Breadcrumb(
                    title=self.get_collection_list_title(), url=self.get_collection_list_url()
                )
            )

        if self.collection_include_detail_crumb():
            breadcrumb.append(
                Breadcrumb(
                    title=self.get_collection_detail_title(),
                    url=self.get_collection_detail_url(),
                )
            )

        return breadcrumb

    def get_titlebuttons(self):
        buttons = super().get_titlebuttons()

        if self.collection_include_add_titlebutton():
            buttons.append(
                TitleButton(
                    url=self.get_collection_add_url(),
                    label=self.get_collection_add_titlebutton_label(),
                )
            )

        return buttons

    def get_table_class(self):
        """
        This method returns the django-tables2 Table class to use in the list view.
        If no class is defined, a new Table class is created (with one linked column).
        """
        if self.table_class:
            return self.table_class

        if not hasattr(self, "_table_class"):

            class CollectionTable(tables.Table):
                item = tables.LinkColumn(
                    self.collection_detail_urlname,
                    args=(tables.A("pk"),),
                    verbose_name=self.get_model_verbose_name(),
                    text=lambda obj: str(obj),
                    accessor=tables.A("pk"),
                )

            self._table_class = CollectionTable

        return self._table_class

    def collection_include_add_titlebutton(self):
        """
        If this method returns true, an "Add model verbose name" button should be
        included in the list view.
        """
        return issubclass(self.__class__, CruditorListView) and self.collection_add_urlname

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
            self.collection_include_list_crumb()
            and not issubclass(self.__class__, (CruditorAddView, CruditorChangeView))
            and hasattr(self, "object")
        )

    def get_collection_url_args(self):
        """
        This helper method returns the args that are used to reverse urls for
        list and add views (views that don't refer to a object/instance).
        By default, returns an empty tuple.
        """
        return ()

    def get_collection_object_url_args(self):
        """
        This helper method returns the args that are used to reverse urls for
        views that refer to a detail page (object/instance related views).
        By default returns the object PK.
        """
        return (self.object.pk,)

    def get_collection_list_title(self):
        """
        Helper method to override the used collection list title.
        By default, just returns the class ``collection_list_title`` property.
        """
        return self.collection_list_title

    def get_collection_list_url(self):
        """
        Helper method to generate the collection list url.
        By default, just calls reverse with the ``collection_list_urlname`` property.
        """
        return reverse(self.collection_list_urlname, args=self.get_collection_url_args())

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
        return reverse(
            self.collection_detail_urlname, args=self.get_collection_object_url_args()
        )

    def get_collection_add_titlebutton_label(self):
        """
        Helper method to override the used button label for the "Add" title button.
        By default, returns "Add <model verbose name>".
        """
        return gettext("Add {0}").format(self.get_model_verbose_name())

    def get_collection_add_url(self):
        """
        Helper method to generate the collection add url.
        By default, just calls reverse with the ``collection_add_urlname`` property.
        """
        return reverse(self.collection_add_urlname, args=self.get_collection_url_args())

    def get_collection_delete_url(self):
        """
        Helper method to generate the collection delete url for the current object.
        By default, calls reverse with the ``collection_delete_urlname`` property
        and passes the object pk to the function call.
        """
        return reverse(
            self.collection_delete_urlname, args=self.get_collection_object_url_args()
        )

    def get_collection_object_success_url(self):
        """
        Helper method to generate the success url after obejct related redirects (e.g. add, change).
        By default, calls reverse with the ``get_collection_list_url`` method.
        """
        return self.get_collection_list_url()


def generate_urls(
    path_prefix,
    name_prefix,
    list_view=None,
    add_view=None,
    change_view=None,
    delete_view=None,
    extra_detail_views=None,
    detail_path="<int:pk>",
):
    """
    This helper allows creating urls for urlpatterns in urls.py in a fast way by just providing
    the view classes and some url and name prefix. In addition, one can add extra detail views.
    """
    if path_prefix and path_prefix[-1] != "/":
        path_prefix = f"{path_prefix}/"

    detail_path = detail_path.strip("/")

    def build_path(path):
        new_path = f"{path_prefix}{path}"
        if not settings.APPEND_SLASH:
            new_path = new_path.strip("/")
        elif new_path and new_path[-1] != "/":
            new_path = f"{new_path}/"

        return new_path

    def build_name(name):
        return f"{name_prefix}{name}"

    urls = []

    if list_view:
        urls.append(path(build_path(""), list_view.as_view(), name=build_name("list")))

    if add_view:
        urls.append(path(build_path("add"), add_view.as_view(), name=build_name("add")))

    if change_view:
        urls.append(
            path(build_path(detail_path), change_view.as_view(), name=build_name("change"))
        )

    if delete_view:
        urls.append(
            path(
                build_path(f"{detail_path}/delete"),
                delete_view.as_view(),
                name=build_name("delete"),
            )
        )

    for name, view in (extra_detail_views or {}).items():
        urls.append(
            path(build_path(f"{detail_path}/{name}"), view.as_view(), name=build_name(name))
        )

    return urls
