from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/create$', views.createuser),
    url(r'^user/login$', views.login),
    url(r'^show$', views.show),
    url(r'^logout$', views.logout),
    url(r'^appointment/add$', views.create),
    url(r'^appointments/(?P<id>\d+)$', views.edit),
    url(r'^appointments/(?P<id>\d+)/update$', views.update),
    url(r'^appointments/delete/(?P<id>\d+)$', views.delete),
]
