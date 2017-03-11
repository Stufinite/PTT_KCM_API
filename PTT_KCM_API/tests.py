from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

# Create your tests here.
class ApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_date(self):
        import json, re

        Month2Num = {
            "Jan" : 1,
            "Feb" : 2,
            "Mar" : 3,
            "Apr" : 4,
            "May" : 5,
            "Jun" : 6,
            "Jul" : 7,
            "Aug" : 8,
            "Sep" : 9,
            "Oct" : 10,
            "Nov" : 11,
            "Dec" : 12
        }

        response = self.client.get(reverse('PTT_KCM_API:articles')+"?issue=黑特&date=2006-9")
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content.decode('utf-8'))
        pttDate = re.split('\s+', j[0]['date'])
        self.assertEqual((9 == int(Month2Num[pttDate[1]]) and 2006 == int(pttDate[-1])), True)
        self.assertEqual('黑特' in str(json.loads(response.content.decode('utf-8'))), True)

    def test_articles(self):
        import json
        response = self.client.get(reverse('PTT_KCM_API:articles')+"?issue=黑特")
        self.assertEqual(response.status_code, 200)
        self.assertEqual('黑特' in str(json.loads(response.content.decode('utf-8'))), True)


    def test_ip(self):
        import json
        response = self.client.get(reverse('PTT_KCM_API:ip')+"?issue=黑特")
        j = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
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
        j = json.loads(response.content.decode('utf-8'))
        self.assertEqual("map" in j, True)
        self.assertEqual(response.status_code, 200)
