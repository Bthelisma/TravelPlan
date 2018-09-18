from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home),
    url(r'^index', views.index),
    url(r'^register$', views.register),
    url(r'^travel$', views.travel),
    url(r'^addplan$', views.addplan),
    url(r'^createplan$', views.createplan),
    url(r'^trip/(?P<travel_id>\d+)$', views.show),
    url(r'^join/(?P<travel_id>\d+)$', views.join),
    url(r'^remove/(?P<travel_id>\d+)$', views.remove),
    url(r'^delete/(?P<travel_id>\d+)$', views.delete),
    url(r'^login$', views.login),
    url(r'^guest_login$', views.guest_login),
    url(r'^logout$', views.logout),
]
