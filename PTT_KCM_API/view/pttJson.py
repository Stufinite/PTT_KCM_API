import json
from datetime import datetime, date
from PTT_KCM_API.models import IpTable, IP
from PTT_KCM_API.dbip_apiKey import apiKey
from pymongo import MongoClient
from project.settings_database import uri
from PTT_KCM_API.view.ip_request import getIPLocation

class pttJson(object):
	""" A pttJson object having api for web to query
	Args:
		filePath: path to ptt json file.

	Returns:
		ptt articles with specific issue.
	"""
	def __init__(self, filePath='ptt-web-crawler/HatePolitics-1-3499.json', uri=uri):
		self.filePath = filePath
		self.InputdirPath = 'PTT_KCM_API/RawIpInput/'
		self.Month2Num = {
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
		self.client = MongoClient(uri)
		self.db = self.client['ptt']
		self.collect = None

	def __getCollect(self, typeOfFile):
		if typeOfFile != 'locations' and typeOfFile != 'ip' and typeOfFile != 'articles' and typeOfFile!='tfidf':
			raise Exception('typeOfFile ERROR')
		return self.db[typeOfFile]

	def getArticleWithIssue(self, issue, date, typeOfFile = "articles"):
		import re
		articleLists = []
		start = False if date.date() != datetime.today().date() else True

		for i in list(self.db['invertedIndex'].find({'issue':issue}, {"ObjectID":1, '_id': False}).limit(1))[0]['ObjectID']:
			art = list(self.db['articles'].find({"_id":i}, {'_id': False}).limit(1))[0]
			try:
				pttDate = re.split('\s+', art.get('date', ''))
				# \s : 比對任一個空白字元（White space character），等效於 [ \f\n\r\t\v]
				if pttDate == ['']: continue
				if start or (date.month == int(self.Month2Num[pttDate[1]]) and date.year == int(pttDate[-1])):
					articleLists.append(art)
			except Exception as e:
				with open('error.log', 'a', encoding='utf8') as f:
					f.write(str(e)+'\n')
					f.write('---------------------------------\n')
					f.write(str(i)+'\n')

		return articleLists

	def save2DB(self, issue, typeOfFile, file, datetime):
		datetime = 'all' if datetime.date() == datetime.today().date()  else str(datetime.date())

		collect = self.__getCollect(typeOfFile)
		collect.update({'issue':issue}, {'$set':{datetime : file}}, upsert=True)

	def getFromDB(self, issue, typeOfFile, datetime):
		datetime = 'all' if datetime.date() == datetime.today().date()  else str(datetime.date())

		collect = self.__getCollect(typeOfFile)
		cursor = collect.find({ "$and":[{'issue':issue}, {datetime:{'$exists':True}}] }, {datetime:1, '_id': False}).limit(1)
		if cursor.count() == 0:
			return {}
		return list(cursor)[0][datetime]

	def hasFile(self, issue, typeOfFile, datetime):
		datetime = 'all' if datetime.date() == datetime.today().date()  else str(datetime.date())

		collect = self.__getCollect(typeOfFile)
		cursor = collect.find({ "$and":[{'issue':issue}, {datetime:{'$exists':True}}] }).limit(0)
		if cursor.count() == 0:
			return False
		return True
	def build_IpTable(self):
		def getUserID(IdStr):
			index = IdStr.find('(')
			if index != -1:
				IdStr = IdStr[:index]
			IdStr = IdStr.strip()
			return IdStr

		def Ip2City(ip):
			import time, requests
			dbip = getIPLocation(ip)
			ipDict = dict(
				ip = ip,
				countryName = dbip['countryName'],
				stateProv = dbip['stateProv'],
				city = dbip['city'],
				continentName = 'AAA'
			)
			time.sleep(3)
			print("success!")
			return ipDict
	
		for art in self.db['articles'].find().batch_size(30):
			try:
				try:
					ip_find = IP.objects.get(ip = art['ip'])
				except Exception as e:
					ip_find = None
				if "error" not in art and art['ip'].find('.') != -1 and (ip_find == None or (ip_find.stateProv !="Taiwan Province" and ip_find.continentName != 'AAA')):
					userObj, created = IpTable.objects.get_or_create(
						userID = getUserID(art['author']),
						defaults={ 
							'userID' : getUserID(art['author']),
							'mostFreqCity' : ""
						}
					)

					ipObj, created = IP.objects.update_or_create(
						ip = art['ip'],
						defaults = Ip2City(art['ip'])
					)
					userObj.ipList.add(ipObj)
			except Exception as e:
				print(e)
				print("error")