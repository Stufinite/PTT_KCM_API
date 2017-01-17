def trigger_cache():
	import requests, urllib
	url = 'http://140.120.13.243:8000/PTT_KCM_API/buildArticle2DB'
	re = requests.get(url)
	print(re.text)
trigger_cache()