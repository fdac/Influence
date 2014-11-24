import sys
import json

fn1 = sys.argv[1]
fn2 = sys.argv[2]

f1 = open(fn1, 'r').read()
f2 = open(fn2, 'r').read()

js1 = json.loads(f1)
js2 = json.loads(f2)

for user in js1:
	if user in js2:
		print user
