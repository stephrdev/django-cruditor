from django.contrib import admin
from django.urls import include, path

from .views import ChangePasswordView, ForbiddenView, HomeView, LogoutView, NotFoundView


handler403 = ForbiddenView.as_view()
handler404 = NotFoundView.as_view()


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('minimal/', include('minimal.urls')),
    path('collection/', include('collection.urls')),
    path('formset/', include('formset.urls')),
    path('remote/', include('remote.urls')),
]
