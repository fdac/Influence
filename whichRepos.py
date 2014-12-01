import pymongo, json

repos = {}
repos['repos'] = []
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
commits = db['commits']

iterator = commits.find({})
for result in iterator:
	try:
		repo = result['values'][0]['repository']['full_name']
		if not repo in repos['repos']:
			repos['repos'].append(repo)
	except KeyError:
		pass

print json.dumps(repos)
