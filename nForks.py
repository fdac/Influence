import pymongo, json

users = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
forks = db['forks']
f = open('data/repList.data', 'r')
replist = json.loads(f.read())

iterator = forks.find({})
for result in iterator:
	try:
		for fork in result['values']:
			repo = ''
			username = ''
			try:
				repo = fork['full_name']
				username = fork['owner']['username']
			except KeyError:
				pass

			if username != '' and repo != '' and repo in replist:
				try:
					users[username] += 1
				except KeyError:
					users[username] = 1
	except KeyError:
		pass

print json.dumps(users)
