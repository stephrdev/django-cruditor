from django.conf.urls import url

from .views import PersonAddView, PersonChangeView, PersonListView


app_name = 'formset'
urlpatterns = [
    url('^$', PersonListView.as_view(), name='list'),
    url('^add/$', PersonAddView.as_view(), name='add'),
    url('^(?P<pk>\d+)/$', PersonChangeView.as_view(), name='change'),
]
