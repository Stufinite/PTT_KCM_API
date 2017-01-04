def trigger_cache():
	import requests, urllib
	with open('PTT_KCM_API/trigger_cache/issue.txt', 'r', encoding='utf8') as f:
		for i in f:
			i = i.strip()
			print(i)
			url = 'http://140.120.13.243:8000/PTT_KCM_API/api/locations/?issue={}'.format(urllib.parse.quote(i))
			re = requests.get(url)