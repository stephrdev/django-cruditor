from django.conf.urls import include, url
from django.contrib import admin

from .views import ChangePasswordView, ForbiddenView, HomeView, LogoutView, NotFoundView


handler403 = ForbiddenView.as_view()
handler404 = NotFoundView.as_view()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^change-password/', ChangePasswordView.as_view(), name='change-password'),
    url(r'^minimal/', include('examples.minimal.urls')),
    url(r'^collection/', include('examples.collection.urls')),
    url(r'^formset/', include('examples.formset.urls')),
    url(r'^remote/', include('examples.remote.urls')),
]
