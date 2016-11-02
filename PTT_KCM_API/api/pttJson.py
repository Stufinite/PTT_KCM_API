import json
from PTT_KCM_API.models import IpTable, IP
from PTT_KCM_API.dbip_apiKey import apiKey

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
		self.json = self._get_pttJson()

	def _get_pttJson(self):
		with open(self.filePath, 'r', encoding='utf8') as f:
			result = json.load(f)
		return result

	def get_articles(self):
		return self.articleLists

	def fileter_with_issue(self, issue):
		try:	
			self.articleLists = [] 
			for i in self.json['articles']:
				if issue in i['article_title'] or issue in i['content']:
					self.articleLists.append(i)
		except Exception as e:
			print(e)

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
				pass

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
		countryName = dbip['countryName'],
		stateProv = dbip['stateProv'],
		city = dbip['city']
		continentName = dbip['continentName']
	)
	return ipDict