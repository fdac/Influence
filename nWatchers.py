import pymongo, json

repos = {}
users = {}
client = pymongo.MongoClient(host='da0.eecs.utk.edu')
db = client['bitbucket']
commits = db['commits']
watchers = db['watchers']

begin = 'https://api.bitbucket.org/2.0/repositories/'
end = '/watchers/'

iterator = watchers.find({})
for result in iterator:
	try:
		repo = result['url'][len(begin):len(result['url'])-len(end)+1]
		repos[repo] = {}
		repos[repo]['watchers'] = len(result['values'])
	except KeyError:
		pass

iterator = commits.find({})
for result in iterator:
	try:
		for commit in result['values']:
			repo = ''
			author = ''
			try:
				repo = commit['repository']['full_name']
				author = commit['author']['username']
			except KeyError:
				pass

			if repo != '' and author != '':
				try:
					repos[repo][author] += 1
				except KeyError:
					repos[repo][author] = 1
			
	except KeyError:
		pass

print json.dumps(repos)
