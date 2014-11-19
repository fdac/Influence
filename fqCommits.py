import pymongo, json, datetime

users = {}
freqs = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
commits = db['commits']

result = commits.find_one({})
year, month, date = map(int, result['values'][0]['date'].split('T')[0].split('-'))

iterator = commits.find({})
i = 0
for result in iterator:
	username = ''
	date = ''
	try:
		username = result['values'][0]['author']['user']['username']
		date = result['values'][0]['date']
	except KeyError:
		pass

	if username != '' and date != '':
		year, month, day = map(int, date.split('T')[0].split('-'))
		u_date = datetime.date(year, month, day)

		try:
			users[username]
		except KeyError:
			users[username] = {
				'commits' : 0,
				'first' : datetime.date(datetime.MAXYEAR, 1, 1),
				'last' : datetime.date(datetime.MINYEAR, 1, 1)
			}

		users[username]['commits'] += 1
		
		if u_date < users[username]['first']:
			users[username]['first'] = u_date

		if u_date > users[username]['last']:
			users[username]['last'] = u_date

for username in users:
	diff = users[username]['last'] - users[username]['first']
	diff = int(diff.days)
	freqs[username] = users[username]['commits'] / (diff + 1)

print json.dumps(freqs)
