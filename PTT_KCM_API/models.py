from django.db import models
from decimal import Decimal

# Create your models here.
class IP(models.Model):
	ip = models.CharField(max_length=15)
	continentName = models.CharField(max_length=15, default='')
	countryName = models.CharField(max_length=20, default='')
	stateProv = models.CharField(max_length=30, default='')
	city = models.CharField(max_length=30, default='')
	def __str__(self):
		return self.ip

class IpTable(models.Model):
	userID = models.CharField(max_length=20)
	mostFreqCity = models.CharField(max_length=20)
	ipList = models.ManyToManyField(IP)
	def __str__(self):
		return self.userID

class Ip2location(models.Model):
	ip_from = models.DecimalField(max_digits=10, decimal_places=0)
	ip_to = models.DecimalField(max_digits=10, decimal_places=0)
	country_code = models.CharField(max_length=2)
	countryName = models.CharField(max_length=64)
	city = models.CharField(max_length=128)
	area = models.CharField(max_length=128)
	def __str__(self):
		return self.ip_from