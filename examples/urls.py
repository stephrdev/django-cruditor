from django.conf.urls import include, url
from django.contrib import admin

from .views import ChangePasswordView, ForbiddenView, HomeView, LogoutView, NotFoundView


handler403 = ForbiddenView.as_view()
handler404 = NotFoundView.as_view()


urlpatterns = [
    url('^admin/', admin.site.urls),

    url('^$', HomeView.as_view(), name='home'),
    url('^logout/', LogoutView.as_view(), name='logout'),
    url('^change-password/', ChangePasswordView.as_view(), name='change-password'),

    url('^minimal/', include('examples.minimal.urls')),
    url('^collection/', include('examples.collection.urls')),
    url('^formset/', include('examples.formset.urls')),
    url('^remote/', include('examples.remote.urls')),
]
