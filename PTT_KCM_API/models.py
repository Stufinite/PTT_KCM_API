from django.db import models

# Create your models here.
class IP(models.Model):
	ip = models.CharField(max_length=15)
	continentName = models.CharField(max_length=15)
	countryName = models.CharField(max_length=20)
	stateProv = models.CharField(max_length=30)
	city = models.CharField(max_length=30)
	def __str__(self):
		return self.ip

class IpTable(models.Model):
	userID = models.CharField(max_length=20)
	mostFreqCity = models.CharField(max_length=20)
	ipList = models.ManyToManyField(IP)
	def __str__(self):
		return self.userID