from django.urls import path

from .views import (
    PersonAddView,
    PersonChangeView,
    PersonDeleteView,
    PersonFilterView,
    PersonListView,
)

app_name = "collection"
urlpatterns = [
    path("", PersonListView.as_view(), name="list"),
    path("filter/", PersonFilterView.as_view(), name="filter"),
    path("add/", PersonAddView.as_view(), name="add"),
    path("<int:pk>/", PersonChangeView.as_view(), name="change"),
    path("<int:pk>/delete/", PersonDeleteView.as_view(), name="delete"),
]
