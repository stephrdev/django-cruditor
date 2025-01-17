from cruditor.datastructures import NavigationDivider, NavigationGroup, NavigationItem
from django.urls import reverse, reverse_lazy


class ExamplesMixin:
    menu_title = "Examples Demo"
    index_url = reverse_lazy("home")
    logout_url = reverse_lazy("logout")
    change_password_url = reverse_lazy("change-password")

    def get_navigation(self):
        return [
            NavigationItem(name="Minimal demo", url=reverse("minimal:demo")),
            NavigationGroup(
                name="Collection",
                items=[
                    NavigationItem(name="Person list", url=reverse("collection:list")),
                    NavigationItem(
                        name="Filter persons",
                        url=reverse("collection:filter"),
                        help_text="Filter persons in a list view",
                    ),
                    NavigationDivider(),
                    NavigationItem(name="Add new person", url=reverse("collection:add")),
                ],
            ),
            NavigationGroup(
                name="Formset",
                items=[
                    NavigationItem(name="Person list", url=reverse("formset:list")),
                    NavigationItem(name="Add new person", url=reverse("formset:add")),
                ],
            ),
            NavigationGroup(
                name="Remote Data",
                items=[
                    NavigationItem(name="Show pets", url=reverse("remote:list")),
                    NavigationItem(name="Add new pet", url=reverse("remote:add")),
                ],
            ),
        ]
