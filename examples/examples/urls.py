from django.contrib import admin
from django.urls import include, path

from .views import ChangePasswordView, ForbiddenView, LogoutView, NotFoundView


handler403 = ForbiddenView.as_view()
handler404 = NotFoundView.as_view()


urlpatterns = [
    path('admin/', admin.site.urls),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('minimal/', include('minimal.urls')),
]
