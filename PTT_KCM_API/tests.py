from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

# Create your tests here.
class ApiTestCase(TestCase):
	def setUp(self):
		self.client = Client()

	def test_articles(self):
		response = self.client.get(reverse('PTT_KCM_API:articles')+"?issue=黑特")
		self.assertEqual(response.status_code, 200)

	def test_ip(self):
		response = self.client.get(reverse('PTT_KCM_API:ip')+"?issue=黑特")
		self.assertEqual(response.status_code, 200)

	def test_locations(self):
		response = self.client.get(reverse('PTT_KCM_API:locations')+"?issue=黑特")
		self.assertEqual(response.status_code, 200)
