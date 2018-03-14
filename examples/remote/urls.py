from django.urls import path

from .views import PetAddView, PetChangeView, PetDeleteView, PetListView


app_name = 'remote'
urlpatterns = [
    path('', PetListView.as_view(), name='list'),
    path('add/', PetAddView.as_view(), name='add'),
    path('<int:pk>/', PetChangeView.as_view(), name='change'),
    path('<int:pk>/delete/', PetDeleteView.as_view(), name='delete'),
]
