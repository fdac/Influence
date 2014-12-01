import pymongo, json, datetime

users = {}
freqs = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
commits = db['commits']
f = open('data/repList.data', 'r')
replist = json.loads(f.read())

iterator = commits.find({})
for result in iterator:
	try:
		for commit in result['values']:
			username = ''
			repo = ''
			date = ''
			try:
				username = commit['author']['user']['username']
				repo = commit['repository']['full_name']
				date = commit['date']
			except KeyError:
				pass
	
			if username != '' and date != '' and repo != '' and repo in replist['repos']:
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
	except KeyError:
		pass

for username in users:
	diff = users[username]['last'] - users[username]['first']
	diff = int(diff.days)
	freqs[username] = 1.0*users[username]['commits'] / (diff + 1)

print json.dumps(freqs)
