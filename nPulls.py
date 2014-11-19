import pymongo, json

users = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
pulls = db['pullrequests']

iterator = pulls.find({})
for result in iterator:
	try:
		for pull in result['values']:
			username = ''
			try:
				author = pull['author']
				if author != None:
					username = author['username']
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
