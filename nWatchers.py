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
i = 0
for result in iterator:
	if i > 5000:
		break
	i += 1
	try:
		for commit in result['values']:
			repo = ''
			author = ''
			try:
				repo = commit['repository']['full_name']
				author = commit['author']['user']['username']
			except KeyError:
				pass

			if repo != '' and author != '':
				try:
					repos[repo][author] += 1
				except KeyError:
					repos[repo][author] = 1
			
	except KeyError:
		pass

for repo in repos:
	total = 0
	for author in repos[repo]:
		if author != 'watchers':
			total += repos[repo][author]
	
	for author in repos[repo]:
		if author != 'watchers':
			try:
				users[author] += 1.0 * repos[repo]['watchers'] * repos[repo][author] / (total + 1)
			except KeyError:
				users[author] = 1.0 * repos[repo]['watchers'] * repos[repo][author] / (total + 1)

print json.dumps(users)
