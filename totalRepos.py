import pymongo, json

users = {}
totals = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
commits = db['commits']

print commits.find_one({})['values'][0]['repository']['name']
iterator = commits.find({})
for result in iterator:
	try:
		for commit in result['values']:
			username = ''
			reponame = ''
			try:
				username = commit['author']['user']['username']
				reponame = commit['repository']['name']
			except KeyError:
				pass
	
			if username != '' and reponame != '':
				try:
					users[username]
				except KeyError:
					users[username] = {
						'count' : 0,
						'repos' : []
					}

				if not reponame in users[username]['repos']:
					users[username]['count'] += 1
					users[username]['repos'].append(reponame)

	except KeyError:
		pass

for username in users:
	totals[username] = users[username]['count']
print json.dumps(users)
