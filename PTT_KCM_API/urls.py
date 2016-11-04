# -*- coding: utf-8 -*-
from django.conf.urls import url
from PTT_KCM_API import views
urlpatterns = [
	url(r'^api/articles/$', views.articles, name='articles'), # api that returns PTT articles.
	url(r'^api/ip/$', views.ip, name='ip'), # api that returns comments with ip.
	url(r'^api/locations/$', views.locations, name='locations'), # api that returns comments with city in a Taiwan.
	url(r'^build_IpTable/$', views.build_IpTable, name='build_IpTable'), # build IpTable.
	url(r'^build_IpTable_with_IpList1/$', views.build_IpTable_with_IpList1, name='build_IpTable_with_IpList1'), # build IpTable.
	url(r'^build_IpTable_with_IpList2/$', views.build_IpTable_with_IpList2, name='build_IpTable_with_IpList2'), # build IpTable.
	url(r'^putintodb/$', views.putintodb, name='putintodb'), # build IpTable.
]