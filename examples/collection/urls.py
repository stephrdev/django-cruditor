from django.conf.urls import url

from .views import (
    PersonAddView, PersonChangeView, PersonDeleteView, PersonFilterView, PersonListView)


app_name = 'collection'
urlpatterns = [
    url('^$', PersonListView.as_view(), name='list'),
    url('^filter/$', PersonFilterView.as_view(), name='filter'),
    url('^add/$', PersonAddView.as_view(), name='add'),
    url('^(?P<pk>\d+)/$', PersonChangeView.as_view(), name='change'),
    url('^(?P<pk>\d+)/delete/$', PersonDeleteView.as_view(), name='delete'),
]
