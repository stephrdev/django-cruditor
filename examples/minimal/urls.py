from django.conf.urls import url

from .views import DemoView


app_name = 'minimal'
urlpatterns = [
    url('^$', DemoView.as_view(), name='demo'),
]
