from rest_framework import routers
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'output/*(?P<date>[0-9-]+)*', views.output, name='output'),
    url(r'settings', views.settings, name='settings'),
    url(r'sleep', views.sleep, name='sleep'),
    url(r'download', views.download, name='download'),
]