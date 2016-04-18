from django.conf.urls import url

from .views import LogoutView, UserChangeView, UserListView


handler403 = 'authinterface.views.no_permission_view'
handler404 = 'authinterface.views.not_found_view'


urlpatterns = [
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^$', UserListView.as_view(), name='user-list'),
    url(r'^(?P<pk>\d+)/$', UserChangeView.as_view(), name='user-change'),
]
