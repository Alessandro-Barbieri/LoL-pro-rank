import json
import csv
from operator import itemgetter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot
from matplotlib.dates import date2num

giocatori1 = {}
filename = 'lol pro rank - Foglio5.csv'
with open(filename, 'rt', encoding = 'utf-8-sig') as f:
	reader = csv.reader(f)

	for riga in reader:
		giocatori1[riga[1]] = (riga[2], riga[3])

inv_giocatori1 = {}
for k, v in giocatori1.items():
	inv_giocatori1.setdefault(v[0], []).append(k)

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

N=50
xN = 2
yN = 60
matplotlib.rc('font', family = 'Unifont')

pyplot.figure(1)
params = pyplot.gcf()
plSize = params.get_size_inches()
params.set_size_inches((plSize[0]*xN, plSize[1]*yN))

err = [c[3] for c in ordinati]
pyplot.errorbar([c[2] for c in ordinati], conteggio, xerr = err, fmt = 'ro')

pyplot.grid(which='both', axis='both')
pyplot.yticks(conteggio, ['/'.join(inv_giocatori1[c[0]]) for c in ordinati])
pyplot.tick_params(axis = 'both', labelsize = 'large')
pyplot.savefig("test.pdf", format = "pdf")

pyplot.figure(2)

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
pyplot.savefig("test1.pdf", format = "pdf")
#pyplot.show()
