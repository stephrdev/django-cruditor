from cruditor.collection import generate_urls
from django.urls import path

from .views import (
    PersonAddView,
    PersonChangeView,
    PersonDeleteView,
    PersonFilterView,
    PersonListView,
)

app_name = "collection"
urlpatterns = generate_urls(
    "", "", PersonListView, PersonAddView, PersonChangeView, PersonDeleteView
) + [
    path("filter/", PersonFilterView.as_view(), name="filter"),
]
