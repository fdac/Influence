import pymongo, json

users = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
followers = db['followers']

iterator = followers.find({})
for result in iterator:
	try:
		username = result['url'].lstrip('https://bitbucket.org/api/2.0/users/').rstrip('/followers')
		if username != '':
			users[username] = len(result['values'])
	except KeyError:
		pass

print json.dumps(users)
