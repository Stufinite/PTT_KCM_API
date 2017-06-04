# -*- coding: utf-8 -*-
from django.conf.urls import url
from PTT_KCM_API import views

urlpatterns = [
	url(r'^api/articles/$', views.articles, name='articles'), # api that returns PTT articles.
	url(r'^api/ip/$', views.ip, name='ip'), # api that returns comments with ip.
	url(r'^api/locations/$', views.locations, name='locations'), # api that returns comments with city in a Taiwan.
	url(r'^api/tfidf/$', views.tfidf, name='tfidf'), # api that returns comments with city in a Taiwan.
]