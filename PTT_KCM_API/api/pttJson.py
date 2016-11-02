import json
from PTT_KCM_API.models import IpTable, IP
class pttJson(object):
	""" A pttJson object having api for web to query
	Args:
		filePath: path to ptt json file.

	Returns:
		ptt articles with specific issue.
	"""
	def __init__(self, filePath='ptt-web-crawler/HatePolitics-1-3499.json'):
		self.filePath = filePath
		self.articleLists = []
		self.json = self._get_pttJson()

	def _get_pttJson(self):
		with open(self.filePath, 'r', encoding='utf8') as f:
			result = json.load(f)
		return result

	def get_articles(self):
		return self.articleLists

	def fileter_with_issue(self, issue):
		try:
			for i in self.json['articles']:
				if issue in i['article_title'] or issue in i['content']:
					self.articleLists.append(i)
		except Exception as e:
			pass

	def build_IpTable(self):
		for i in self.json['articles']:
			try:
				if  "error" not in i:
					userObj, created = IpTable.objects.get_or_create(
						userID = i['author'].split(' ')[0],
						defaults={ 
							'userID' : i['author'].split(' ')[0],
							'mostFreqCity' : ""
						}
					)

					ipObj, created = IP.objects.get_or_create(
						ip = i['ip'],
						defaults = {
							'ip' : i['ip'],
							'city' : ""
						}
					)
					userObj.ipList.add(ipObj)
			except Exception as e:
				pass