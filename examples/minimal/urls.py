from django.urls import path

from .views import DemoView


app_name = 'minimal'
urlpatterns = [
    path('', DemoView.as_view(), name='demo'),
]
