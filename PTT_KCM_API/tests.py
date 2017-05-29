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
        self.assertEqual(response.json(), [{'article_id': 'M.1474380408.A.0F2', 'date': 'Tue Sep 20 22:06:45 2016', 'article_title': '[震怒] 我的噴火龍呢?', 'ip': '122.100.79.113', 'message_conut': {'push': 2, 'count': 1, 'neutral': 0, 'boo': 1, 'all': 3}, 'messages': [{'push_tag': '推', 'push_userid': 'sheng945', 'push_ipdatetime': '118.150.13.245 09/20 22:07', 'push_content': ['噴火', '太慢', '抓到', '北投', '上次']}, {'push_tag': '噓', 'push_userid': 'boy9501', 'push_ipdatetime': '27.242.42.233 09/20 22:10', 'push_content': ['活該', '哈哈哈']}, {'push_tag': '推', 'push_userid': 'dreamcomes', 'push_ipdatetime': '101.13.112.121 09/20 22:11', 'push_content': ['時間', '掌握', '地點']}], 'author': 'J224960607 (你心目中的凱伊)', 'content': ['親愛的', '公車上', '地點', '漸漸', '出現', '聚集', '搭上', '牛鬼蛇神', '抓到', '連單', '紅樹林', '見到', '噴火龍', '抽到', '男友', '公車', '知道', '反省', '這次', '情緒', '下次', '路人', '憤怒', '眼前', '唯一', '回家', '詢問', '逃走', '現在', '不讓', '抱著', '連臉', '附近', '不斷', '所在', '期待', '只能', '懷裡', '看看', '哀傷', '無盡', '月兔', '悲傷', '打轉', '白貓', '黃昏', '不該', '淡大', '散去', '野生', '對待', '奔往', '捷運', '市場', '下車', '是不是', '時經', '畫面', '車窗', '火速', '遊戲', '無能', '無法挽回', '了往', '降臨', '所愛', '今晚', '身上', '進化', '回到', '順利', '抓過', '手機', '看到', '薰香', '導致', '欣喜若狂', '準備', '剩下', '人潮', '依然', '原來'], 'board': 'Hate'}])

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
