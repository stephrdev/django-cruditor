from django.urls import path

from .views import RecordAddView, RecordListView


app_name = 'remote'
urlpatterns = [
    path('', RecordListView.as_view(), name='list'),
    path('add/', RecordAddView.as_view(), name='add'),
]
