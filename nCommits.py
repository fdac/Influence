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
			try:
				username = commit['author']['user']['username']
			except KeyError:
				pass
	
			if username != '':
				try:
					users[username] += 1
				except KeyError:
					users[username] = 1
	except KeyError:
		pass

print json.dumps(users)
