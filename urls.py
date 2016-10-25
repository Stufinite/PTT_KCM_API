# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from PTT_factory import views
urlpatterns = [
	url(r'^api/ip/$', views.ip, name='api_ip'), # api for ip_comment lookup.
]