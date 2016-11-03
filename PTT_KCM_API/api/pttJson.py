import json, requests, os, time
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

	def __get_pttJson(self):
		with open(self.filePath, 'r', encoding='utf8') as f:
			result = json.load(f)
		return result

	def get_articles(self):
		return self.articleLists

	def getIssueFilePath(self, issue, type):
		return '{}/{}/{}.json.{}'.format(self.dirPath, issue, issue, type)

	def getIssueFolderPath(self, issue):
		return '{}/{}'.format(self.dirPath, issue)

	def fileter_with_issue(self, issue, type = "articles"):
		self.articleLists = []
		for i in self.json['articles']:
			try:
				if issue in i.get('article_title', '') or issue in i.get('content', ''):
					self.articleLists.append(i)
			except Exception as e:
				with open('error.log', 'a', encoding='utf8') as f:
					f.write(str(e))
					f.write('---------------------------------\n')
					f.write(str(i))

	def saveFile(self, issue, type, file):
		with open(self.getIssueFilePath(issue, type), 'w', encoding='utf8') as f:
			json.dump(file, f)

	def loadFile(self, filePath):
		with open(filePath, 'r', encoding='utf8') as f:
			return json.load(f)

	def hasFile(self, issue, type):
		file = Path(self.getIssueFilePath(issue, type))
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

	def build_IpTable_with_IpList(self, file):
		ipset = set()
		with open(file, 'r', encoding='utf8') as f:
			for i in f:
				if i.find('.') != -1:
					i = i.replace('\n','')
					ipset.add(i)
		for ip in ipset:
			ipObj, created = IP.objects.update_or_create(
				ip = ip,
				defaults = Ip2City(ip)
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
def Ip2City2(ip):
	dbip = requests.get('http://api.db-ip.com/v2/' + 'ec5942a0169e0ee70284875cfd5dac5f98632750' + '/' + ip)
	dbip = json.loads(dbip.text)
	ipDict = dict(
		ip = ip,
		countryName = dbip['countryName'],
		stateProv = dbip['stateProv'],
		city = dbip['city'],
		continentName = dbip['continentName']
	)
	return ipDict
def Ip2City3(ip):
	dbip = requests.get('http://api.db-ip.com/v2/' + '37c8932b3c75b30e299a1d5e651e2bacff147ea3' + '/' + ip)
	dbip = json.loads(dbip.text)
	ipDict = dict(
		ip = ip,
		countryName = dbip['countryName'],
		stateProv = dbip['stateProv'],
		city = dbip['city'],
		continentName = dbip['continentName']
	)
	return ipDict