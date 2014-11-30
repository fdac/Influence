import pymongo, json

repos = {}
repos['repos'] = []
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
commits = db['commits']

iterator = commits.find({})
for result in iterator:
	try:
		for commit in result['values']:
			repo = ''
			try:
				repo = commit['repository']['full_name']
			except KeyError:
				pass
	
			if repo != '' and not repo in repos['repos']:
				repos['repos'].append(repo)

	except KeyError:
		pass

print json.dumps(repos)
