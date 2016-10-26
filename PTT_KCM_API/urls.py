# -*- coding: utf-8 -*-
from django.conf.urls import url
from PTT_KCM_API import views
urlpatterns = [
	url(r'^api/ip/$', views.ip, name='api_ip'), # api for ip_comment lookup.
]