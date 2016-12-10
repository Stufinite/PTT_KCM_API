import json, requests, os, time, random, re
from datetime import datetime, date
from PTT_KCM_API.models import IpTable, IP
from PTT_KCM_API.dbip_apiKey import apiKey
from pathlib import Path


class pttJson(object):
	""" A pttJson object having api for web to query
	Args:
		filePath: path to ptt json file.

	Returns:
		ptt articles with specific issue.
	"""
	def __init__(self, filePath='ptt-web-crawler/HatePolitics-1-3499.json'):
		self.filePath = filePath
		self.articleLists = ()
		self.json = self.__get_pttJson()
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
		self.length = len(self.json['articles'])

	def __get_pttJson(self):
		with open(self.filePath, 'r', encoding='utf8') as f:
			result = json.load(f)
		return result

	def get_articles(self):
		return self.articleLists

	def getIssueFilePath(self, issue, typeOfFile, date):
		return '{}/{}/{}.json.{}.{}'.format(self.dirPath, issue, issue, typeOfFile, str(date.year)+'-'+str(date.month) if date.date() != datetime.today().date() else 'all')

	def getIssueFolderPath(self, issue):
		return '{}/{}'.format(self.dirPath, issue)

	def filter_with_issue(self, issue, date, typeOfFile = "articles"):
		self.articleLists = []
		start = False if date.date() != datetime.today().date() else True

		for i in self.json['articles']:
			try:
				pttDate = re.split('\s+', i.get('date', ''))
				# \s : 比對任一個空白字元（White space character），等效於 [ \f\n\r\t\v]
				if pttDate == ['']: continue
				if start or (date.month == int(self.Month2Num[pttDate[1]]) and date.year == int(pttDate[-1])):
					if issue in i.get('article_title', '') or issue in i.get('content', ''):
						self.articleLists.append(i)
			except Exception as e:
				with open('error.log', 'a', encoding='utf8') as f:
					f.write(str(e)+'\n')
					f.write('---------------------------------\n')
					f.write(str(i)+'\n')

	def saveFile(self, issue, typeOfFile, file, date):
		with open(self.getIssueFilePath(issue, typeOfFile, date), 'w', encoding='utf8') as f:
			json.dump(file, f)

	def loadFile(self, filePath):
		with open(filePath, 'r', encoding='utf8') as f:
			return json.load(f)

	def hasFile(self, issue, typeOfFile, date):
		file = Path(self.getIssueFilePath(issue, typeOfFile, date))
		if file.is_file():
			return True
		else: return False


	def build_IpTable(self):
		for i in self.json['articles']:
			try:
				if  "error" not in i and i['ip'].find('.') != -1:
					userObj, created = IpTable.objects.get_or_create(
						userID = getUserID(i['author']),
						defaults={ 
							'userID' : getUserID(i['author']),
							'mostFreqCity' : ""
						}
					)

					ipObj, created = IP.objects.update_or_create(
						ip = i['ip'],
						defaults = Ip2City(i['ip'])
					)
					userObj.ipList.add(ipObj)
			except Exception as e:
				print(e)

	def build_IpTable_with_IpList(self, file, key):
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

	def putIntoDB(self, ipjson,):
		with open(self.InputdirPath+ipjson, 'r', encoding='utf8') as f:
			dbip = json.load(f)
			for ipjson in dbip:
				ipObj, created = IP.objects.update_or_create(
					ip = ipjson['ipAddress'],
					defaults = ipGetFromJson(ipjson)
				)


def getUserID(IdStr):
	index = IdStr.find('(')
	if index != -1:
		IdStr = IdStr[:index]
	IdStr = IdStr.strip()
	return IdStr

def Ip2City(ip):
	dbip = requests.get('http://api.db-ip.com/v2/' + apiKey + '/' + ip)
	dbip = json.loads(dbip.text)
	ipDict = dict(
		ip = ip,
		countryName = dbip['countryName'],
		stateProv = dbip['stateProv'],
		city = dbip['city'],
		continentName = dbip['continentName']
	)
	time.sleep(5)
	return ipDict

def Ip2City_from_ipList(ip, key):
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

def ipGetFromJson(ipjson):
	ipDict = dict(
		ip = ipjson['ipAddress'],
		countryName = ipjson['countryName'],
		stateProv = ipjson['stateProv'],
		city = ipjson['city'],
		continentName = ipjson['continentName']
	)
	return ipDict