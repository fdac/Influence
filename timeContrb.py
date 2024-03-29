import pymongo, json, datetime

users = {}
spans = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
commits = db['commits']

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
	
			if username != '' and date != '':
				year, month, day = map(int, date.split('T')[0].split('-'))
				u_date = datetime.date(year, month, day)

				try:
					users[username]
				except KeyError:
					users[username] = {
						'first' : datetime.date(datetime.MAXYEAR, 1, 1),
						'last' : datetime.date(datetime.MINYEAR, 1, 1)
					}

				if u_date < users[username]['first']:
					users[username]['first'] = u_date

				if u_date > users[username]['last']:
					users[username]['last'] = u_date
	except KeyError:
		pass

for username in users:
	diff = users[username]['last'] - users[username]['first']
	diff = int(diff.days)
	spans[username] = diff

print json.dumps(spans)
