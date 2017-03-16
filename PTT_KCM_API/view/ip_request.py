import requests
import sys
from bs4 import BeautifulSoup

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
			city = ipresult.city

		except Exception as e:
			dbip = getIPLocation(ip)
			#dbip = requests.get('http://api.eurekapi.com/iplocation/v1.8/locateip?key=SAKA93BGVHLF2HC88UHZ&ip=' + ip + '&format=JSON')
			#dbip = json.loads(dbip.text)
			countryName = dbip['country_name'],
			city = dbip['city'],
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
		dbip['country_name'] = Location[0].split()[1]
		dbip['stateProv'] = "unknown"
		dbip['city'] = Location[2]
	elif len(Location) == 4:
		dbip['country_name'] = Location[0].split()[1]
		dbip['stateProv'] = Location[1]
		dbip['city'] = Location[3]

	return dbip
