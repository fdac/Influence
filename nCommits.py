import pymongo, json

users = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
commits = db['commits']

iterator = commits.find({})
for result in iterator:
	try:
		for commit in result['values']:
			username = ''
			repo = ''
			try:
				username = commit['author']['user']['username']
				repo = commit['repository']['full_name']
			except KeyError:
				pass
	
			if username != '' and repo != '':
				try:
					users[username] += 1
				except KeyError:
					users[username] = 1
	except KeyError:
		pass

print json.dumps(users)
