import pymongo, json

users = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
pulls = db['pullrequests']
f = open('data/repList.data', 'r')
replist = json.loads(f.read())

iterator = pulls.find({})
for result in iterator:
	try:
		for pull in result['values']:
			username = ''
			repo = ''
			try:
				author = pull['author']
				if author != None:
					username = author['username']
				repo = pull['repository']['full_name']
			except KeyError:
				pass

			if username != '' and repo != '' and repo in replist['repos']:
				try:
					users[username] += 1
				except KeyError:
					users[username] = 1
	except KeyError:
		pass

print json.dumps(users)
