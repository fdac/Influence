import sys
import json
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def normalize(value, iminimum, imaximum):
	mininum = 5
	maximum = 50
	return mininum + ((maximum - mininum) * (value - iminimum) / (imaximum - iminimum))

def make_colormap(seq):
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)

folls = []
wats = []
preds = []

fname = sys.argv[1]

f_pred = open(fname, 'r')
f_fol = open('data/nFollowers.data', 'r')
f_wat = open('data/nWatchers.data', 'r')

js_pred = json.loads(f_pred.read())
js_fol = json.loads(f_fol.read())
js_wat = json.loads(f_wat.read())

min_pred = sys.maxint
max_pred = -sys.maxint-1

for user in js_pred:
	if user in js_fol and user in js_wat:
		folls.append(js_fol[user])
		wats.append(js_wat[user])
		preds.append(js_pred[user])

		if min_pred > js_pred[user]:
			min_pred = js_pred[user]

		if max_pred < js_pred[user]:
			max_pred = js_pred[user]

x = np.array(folls)
y = np.array(wats)
colors = np.array(preds)
sizes = np.array([normalize(item, min_pred, max_pred) for item in preds])

c = mcolors.ColorConverter().to_rgb
rvb = make_colormap([c('red'), c('violet'), 0.33, c('violet'), c('blue'), 0.66, c('blue')])

plt.scatter(x, y, s=sizes, c=colors, cmap=rvb, alpha=0.5, linewidths=0)
plt.colorbar()
plt.title(fname)
plt.xlabel('nFollowers')
plt.ylabel('watchScore')
plt.show()
