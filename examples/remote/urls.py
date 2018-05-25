from django.conf.urls import url

from .views import PetAddView, PetChangeView, PetDeleteView, PetListView


app_name = 'remote'
urlpatterns = [
    url('^$', PetListView.as_view(), name='list'),
    url('^add/$', PetAddView.as_view(), name='add'),
    url('^(?P<pk>\d+)/$', PetChangeView.as_view(), name='change'),
    url('^(?P<pk>\d+)/delete/$', PetDeleteView.as_view(), name='delete'),
]
