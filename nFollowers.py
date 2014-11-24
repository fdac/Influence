import pymongo, json

users = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
followers = db['followers']
head = 'https://bitbucket.org/api/2.0/users/'
tail = '/followers'

iterator = followers.find({})
for result in iterator:
	try:
		username = result['url'][len(head):len(result['url'])-len(tail)]
		if username != '':
			users[username] = len(result['values'])
	except KeyError:
		pass

print json.dumps(users)
