from cruditor.collection import CollectionViewMixin
from cruditor.views import (
    CruditorAddView,
    CruditorChangeView,
    CruditorDeleteView,
    CruditorListView,
)
from django.urls import reverse, reverse_lazy

from examples.mixins import ExamplesMixin

from .forms import PetForm
from .models import Pet


class PetMixin(ExamplesMixin, CollectionViewMixin):
    collection_list_title = "Pets"
    collection_list_urlname = "remote:list"
    collection_detail_urlname = "remote:change"
    collection_delete_urlname = "remote:delete"
    model_verbose_name = "Pet"


class PetListView(PetMixin, CruditorListView):
    def get_titlebuttons(self):
        return [{"url": reverse("remote:add"), "label": "Add pet"}]

    def get_queryset(self):
        return Pet.get_list()


class PetAddView(PetMixin, CruditorAddView):
    form_class = PetForm
    success_url = reverse_lazy("remote:list")
    model_verbose_name = "Pet"


class PetChangeView(PetMixin, CruditorChangeView):
    form_class = PetForm
    success_url = reverse_lazy("remote:list")
    model_verbose_name = "Pet"

    def get_object(self):
        return Pet.get(self.kwargs["pk"])


class PetDeleteView(PetMixin, CruditorDeleteView):
    success_url = reverse_lazy("remote:list")

    def get_object(self):
        return Pet.get(self.kwargs["pk"])
