import json
from operator import itemgetter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot
from matplotlib.dates import date2num

with open('giocatori.json', encoding = 'utf-8-sig') as j:
	mydict2 = json.load(j)

g = []
for p in mydict2.keys():
	mi = mydict2[p][-1][1]
	sigma = mydict2[p][-1][2]
	g.append((p, mi - 2*sigma, mi, 2*sigma))

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
pyplot.yticks(conteggio, ['/'.join(inv_giocatori1[c[0]]) for c in ordinati])
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
	x = [(i[0]) for i in mydict2[g[0]]]
	y = [(i[1] - 2 * i[2]) for i in mydict2[g[0]]]
	l = '/'.join(inv_giocatori1[g[0]])
	pyplot.plot(x, y, '-', drawstyle = 'steps', label = l)

legend = pyplot.legend(loc = 'lower left')
pyplot.tick_params(axis = 'both', labelsize = 'large')
pyplot.savefig("test1.pdf", bbox_inches='tight', format = "pdf")
