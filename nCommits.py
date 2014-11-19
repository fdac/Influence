import pymongo, json

users = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
commits = db['commits']

iterator = commits.find({})
for result in iterator:
	username = ''
	try:
		username = result['values'][0]['author']['user']['username']
	except KeyError:
		pass

	if username != '':
		try:
			users[username] += 1
		except KeyError:
			users[username] = 1

json.dumps(users)
