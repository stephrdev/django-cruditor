from django.urls import path

from .views import PersonAddView, PersonChangeView, PersonListView


app_name = 'formset'
urlpatterns = [
    path('', PersonListView.as_view(), name='list'),
    path('add/', PersonAddView.as_view(), name='add'),
    path('<int:pk>/', PersonChangeView.as_view(), name='change'),
]
