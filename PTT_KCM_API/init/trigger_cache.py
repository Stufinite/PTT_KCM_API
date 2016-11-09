import requests, urllib
with open('issue.txt', 'r', encoding='utf8') as f:
	for i in f:
		print(i)
		i = i.strip()
		url = 'http://140.120.13.243:8000/PTT_KCM_API/api/locations/?issue={}'.format(urllib.parse.quote(i))
		print(url)
		re = requests.get(url)
		# print(re.text)
		print('finish')