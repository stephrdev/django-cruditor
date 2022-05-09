from django.conf.urls import url

from .views import (
    PersonAddView,
    PersonChangeView,
    PersonDeleteView,
    PersonFilterView,
    PersonListView,
)


app_name = 'collection'
urlpatterns = [
    url(r'^$', PersonListView.as_view(), name='list'),
    url(r'^filter/$', PersonFilterView.as_view(), name='filter'),
    url(r'^add/$', PersonAddView.as_view(), name='add'),
    url(r'^(?P<pk>\d+)/$', PersonChangeView.as_view(), name='change'),
    url(r'^(?P<pk>\d+)/delete/$', PersonDeleteView.as_view(), name='delete'),
]
