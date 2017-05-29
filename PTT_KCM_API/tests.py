from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

# Create your tests here.
class ApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_date(self):
        import json, re
        response = self.client.get(reverse('PTT_KCM_API:articles')+"?issue=震怒&date=2016-9")
        self.assertEqual(response.json()[0]['date'], 'Tue Sep 20 22:06:45 2016')

    def test_articles(self):
        import json
        response = self.client.get(reverse('PTT_KCM_API:articles')+"?issue=黑特")
        self.assertEqual('黑特' in response.json()[0]['article_title'] or '黑特' in response.json()[0]['content'], True)


    def test_ip(self):
        response = self.client.get(reverse('PTT_KCM_API:ip')+"?issue=黑特")
        j = response.json()
        self.assertEqual(j['issue'], "黑特")

        self.assertEqual('author' in j, True)
        self.assertEqual('score' in j['author'][0], True)
        self.assertEqual('ip' in j['author'][0], True)
        self.assertEqual('date' in j['author'][0], True)
        self.assertEqual('author' in j['author'][0], True)

        self.assertEqual('attendee' in j, True)
        self.assertEqual('score' in j['attendee'][0], True)
        self.assertEqual('ip' in j['attendee'][0], True)
        self.assertEqual('push_ipdatetime' in j['attendee'][0], True)
        self.assertEqual('push_userid' in j['attendee'][0], True)
        

    def test_locations(self):
        import json
        response = self.client.get(reverse('PTT_KCM_API:locations')+"?issue=黑特")
        j = response.json()
        self.assertEqual("map" in j, True)
