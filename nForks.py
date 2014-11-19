import pymongo, json

users = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
commits = db['forks']

iterator = commits.find({})
for result in iterator:
	try:
		for fork in result['values']:
			username = ''
			try:
				username = fork['owner']['username']
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
