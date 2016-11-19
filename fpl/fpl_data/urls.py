from django.conf.urls import url
from . import views

app_name = 'fpl_data'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
