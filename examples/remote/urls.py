from django.conf.urls import url

from .views import PetAddView, PetChangeView, PetDeleteView, PetListView


app_name = 'remote'
urlpatterns = [
    url(r'^$', PetListView.as_view(), name='list'),
    url(r'^add/$', PetAddView.as_view(), name='add'),
    url(r'^(?P<pk>\d+)/$', PetChangeView.as_view(), name='change'),
    url(r'^(?P<pk>\d+)/delete/$', PetDeleteView.as_view(), name='delete'),
]
