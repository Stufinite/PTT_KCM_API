from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from djangoApiDec.djangoApiDec import getJsonFromApi
import subprocess


# Create your tests here.
class ApiTestCase(TestCase):
	def init(self):
		self.client = Client()

	def test_api_works(self):
		subprocess.call(['rm', '-rf', 'json'])
		response = self.client.get(reverse('PTT_KCM_API:locations')+"?issue=黑特")
		"""Animals that can speak are correctly identified"""
		self.assertEqual(response.status_code, 200)
