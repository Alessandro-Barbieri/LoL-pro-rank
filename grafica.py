import json
from operator import itemgetter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot
from datetime import datetime
from matplotlib.dates import date2num

with open('giocatori.json', encoding = 'utf-8-sig') as j:
	storico = json.load(j)

g = []
for nome, val in storico.items():
	l = sorted(list(val['date'].items()))
	mi = l[-1][1][0]
	sigma = l[-1][1][1]
	g.append((nome, mi - 3*sigma, mi, 3*sigma))

ordinati = sorted(g, key = itemgetter(1) , reverse = False)

lunghezza = len(ordinati)
conteggio = np.arange(lunghezza)

xN = 2
yN = lunghezza * 30 / 800
matplotlib.rc('font', family = 'Unifont')

pyplot.figure(1)
params = pyplot.gcf()
plSize = params.get_size_inches()
params.set_size_inches((plSize[0]*xN, plSize[1]*yN))

err = [c[3] for c in ordinati]
pyplot.errorbar([c[2] for c in ordinati], conteggio, xerr = err, fmt = 'ro')

pyplot.axis('tight')
pyplot.grid(which='both', axis='both')
pyplot.yticks(conteggio, ['/'.join(storico[c[0]]['alias']) for c in ordinati])
pyplot.tick_params(axis = 'both')
pyplot.savefig("test.pdf", format = "pdf", bbox_inches='tight')

pyplot.figure(2)

N=50
xN = 2
yN = 2
params = pyplot.gcf()
plSize = params.get_size_inches()
params.set_size_inches((plSize[0]*xN, plSize[1]*yN))

for g in ordinati[-25:]:
	n = g[0]
	l = sorted(list(storico[n]['date'].items()))
	x = [(datetime.strptime(i[0], '%Y-%m-%d')) for i in l]
	y = [(i[1][0] - 3 * i[1][1]) for i in l]
	l = '/'.join(storico[n]['alias'])
	pyplot.plot(x, y, '-', drawstyle = 'steps', label = l)

legend = pyplot.legend(loc = 'lower left')
pyplot.tick_params(axis = 'both', labelsize = 'large')
pyplot.savefig("test1.pdf", bbox_inches='tight', format = "pdf")
