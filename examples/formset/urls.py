from django.conf.urls import url

from .views import PersonAddView, PersonChangeView, PersonListView


app_name = 'formset'
urlpatterns = [
    url(r'^$', PersonListView.as_view(), name='list'),
    url(r'^add/$', PersonAddView.as_view(), name='add'),
    url(r'^(?P<pk>\d+)/$', PersonChangeView.as_view(), name='change'),
]
