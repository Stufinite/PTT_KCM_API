import requests
import sys
from bs4 import BeautifulSoup
from PTT_KCM_API.models import IP

def build_map(ipList, result):
	''' Create map instance.

	dbip: ip-location json return from dbip api.
	
	if clause: if key name (eq:台南) doesn't exist, then create dict with that key name and calculate score and attendee.
	'''
	for ip, score in ipList:
		if score == 0:
			continue
		try:
			ipresult = IP.objects.get(ip = ip)
			countryName = ipresult.countryName
			stateProv = ipresult.stateProv,
			city = ipresult.city

		except Exception as e:
			dbip = getIPLocation(ip)
			ipObj, created = IP.objects.update_or_create(
				ip = ip,
				defaults = dbip
			)
			countryName = dbip['countryName']
			city = dbip['city']
			stateProv = dbip['stateProv']
			continentName = 'AAA'

		if countryName != "Taiwan":
			continue
		
		result['map'].setdefault(countryName, {})
		result['map'][countryName].setdefault(city, dict(
			positive=0,
			negative=0,
			attendee=0
		))

		if score > 0:
			result['map'][countryName][city]['positive'] += score
		else:
			result['map'][countryName][city]['negative'] += score
		result['map'][countryName][city]['attendee'] += 1
	return result
def getIPLocation(ip):
	# sign in ip2location
	userData = {
		'emailAddress':'j9963232q@gmail.com',
		'password':'thisgame',
		'btnLogin':'Login »',
	}
	rs = requests.session()
	res = rs.post("https://www.ip2location.com/login",data = userData)

	# get ip location info which we want
	payload = {
		'ipAddress': ip,
		'btnLookup':'Search'
	}
	res2 = rs.post("https://www.ip2location.com/demo",data = payload)
	soup = BeautifulSoup(res2.text)
	with open('after_request_page.txt','w') as output:
		output.write(res2.text)
	dbip = {}
	Ip = soup.select('tr')[0].text.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)
	dbip['ip'] = Ip.split()[2]
	Location = soup.select('tr')[1].text.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)
	Location = Location.split(",")
	if len(Location) == 3:
		dbip['countryName'] = Location[0].split()[1]
		dbip['stateProv'] = "unknown"
		dbip['city'] = Location[2].replace(" ","",1)
	elif len(Location) == 4:
		dbip['countryName'] = Location[0].split()[1]
		dbip['stateProv'] = Location[1].replace(" ","",1)
		dbip['city'] = Location[3].replace(" ","",1)

	return dbip
