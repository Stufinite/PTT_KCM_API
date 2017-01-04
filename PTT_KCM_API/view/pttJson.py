import json
from datetime import datetime, date
from PTT_KCM_API.models import IpTable, IP
from PTT_KCM_API.dbip_apiKey import apiKey
from pymongo import MongoClient

class pttJson(object):
	""" A pttJson object having api for web to query
	Args:
		filePath: path to ptt json file.

	Returns:
		ptt articles with specific issue.
	"""
	def __init__(self, filePath='ptt-web-crawler/HatePolitics-1-3499.json', uri=None):
		self.filePath = filePath
		self.dirPath = 'PTT_KCM_API/json'
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
		if typeOfFile != 'locations' and typeOfFile != 'ip' and typeOfFile != 'articles':
			raise Exception('typeOfFile ERROR')
		return self.db[typeOfFile]

	def getArticleWithIssue(self, issue, date, typeOfFile = "articles"):
		import re
		articleLists = []
		start = False if date.date() != datetime.today().date() else True

		for i in list(self.db['invertedIndex'].find({'issue':issue}, {"objectID":1, '_id': False}).limit(1))[0]['objectID']:
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
		collect = self.__getCollect(typeOfFile)
		collect.update({'issue':issue}, {'$set':{str(datetime.date()) : file}}, upsert=True)

	def getFromDB(self, issue, typeOfFile, datetime):
		collect = self.__getCollect(typeOfFile)
		cursor = collect.find({ "$and":[{'issue':issue}, {str(datetime.date()):{'$exists':True}}] }, {str(datetime.date()):1, '_id': False}).limit(1)
		if cursor.count() == 0:
			return {}
		return list(cursor)[0][str(datetime.date())]

	def hasFile(self, issue, typeOfFile, datetime):
		collect = self.__getCollect(typeOfFile)
		cursor = collect.find({ "$and":[{'issue':issue}, {str(datetime.date()):{'$exists':True}}] }).limit(0)
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
			dbip = requests.get('http://api.eurekapi.com/iplocation/v1.8/locateip?key=SAK2469C36HQB53H65RZ&ip=' + ip + '&format=JSON')
			dbip = json.loads(dbip.text)
			ipDict = dict(
				ip = ip,
				countryName = dbip['geolocation_data']['country_name'],
				stateProv = 'Taiwan Province',
				city = dbip['geolocation_data']['city'],
				continentName = dbip['geolocation_data']['continent_name']
			)
			time.sleep(5)
			return ipDict

		for i in list(self.db['invertedIndex'].find({'issue':issue}, {"objectID":1, '_id': False}).limit(1))[0]['objectID']:
			art = list(self.db['articles'].find({"_id":i}, {'_id': False}).limit(1))[0]
			try:
				if  "error" not in art and art['ip'].find('.') != -1:
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

	def build_IpTable_with_IpList(self, file, key):
		def Ip2City_from_ipList(ip, key):
			import random, time, requests
			dbip = requests.get('http://api.db-ip.com/v2/' + key + '/' + ip)
			try:
				dbip = json.loads(dbip.text)
				ipDict = dict(
					ip = ip,
					countryName = dbip['countryName'],
					stateProv = dbip['stateProv'],
					city = dbip['city'],
					continentName = dbip['continentName']
				)
				time.sleep(random.randint(1,5))
				return ipDict
			except Exception as e:
				pass

		ipset = set()
		with open(self.InputdirPath+file, 'r', encoding='utf8') as f:
			for i in f:
				if i.find('.') != -1:
					i = i.replace('\n','')
					ipset.add(i)
		for ip in ipset:
			try:
				ipObj, created = IP.objects.update_or_create(
					ip = ip,
					defaults = Ip2City_from_ipList(ip, key)
				)
			except Exception as e:
				pass

	def putIntoDB(self, ipjson):
		def ipGetFromJson(ipjson):
			ipDict = dict(
				ip = ipjson['ipAddress'],
				countryName = ipjson['countryName'],
				stateProv = ipjson['stateProv'],
				city = ipjson['city'],
				continentName = ipjson['continentName']
			)
			return ipDict

		with open(self.InputdirPath+ipjson, 'r', encoding='utf8') as f:
			dbip = json.load(f)
			for ipjson in dbip:
				ipObj, created = IP.objects.update_or_create(
					ip = ipjson['ipAddress'],
					defaults = ipGetFromJson(ipjson)
				)

