from django.db import models

# Create your models here.
class IP(models.Model):
	ip = models.CharField(max_length=15)
	city = models.CharField(max_length=20)
	def __str__(self):
		return self.ip

class IpTable(models.Model):
	userID = models.CharField(max_length=20)
	mostFreqCity = models.CharField(max_length=20)
	ipList = models.ManyToManyField(IP)
	def __str__(self):
		return self.userID
