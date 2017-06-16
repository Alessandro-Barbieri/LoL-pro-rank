import csv
import pickle
from operator import itemgetter
import matplotlib.pyplot as pyplot
from matplotlib.dates import date2num 
import numpy as np
import matplotlib

giocatori1 = {}
filename = 'lol pro rank - Foglio5.csv'
with open(filename, 'rt', encoding = 'utf-8') as f:
    reader = csv.reader(f)

    for riga in reader:
        giocatori1[riga[1]] = (riga[2], riga[3])

inv_giocatori1 = {}
for k, v in giocatori1.items():
    inv_giocatori1.setdefault(v[0], []).append(k)

pkl_file = open('giocatori.pkl', 'rb')
mydict2 = pickle.load(pkl_file)
pkl_file.close()


ordinati = sorted([(p, \
                    mydict2[p][-1][1] - 2 * mydict2[p][-1][2], \
                    mydict2[p][-1][1], \
                    2 * mydict2[p][-1][2], \
                    ) for p in mydict2.keys()], \
                  key = itemgetter(1) , \
                  reverse = False)

lunghezza = len(ordinati)
conteggio = np.arange(lunghezza)

N=50
matplotlib.rc('font', family = 'Unifont')
pyplot.figure(1)
pyplot.errorbar([c[2] for c in ordinati], \
             conteggio, \
             xerr = [c[3] for c in ordinati], \
             fmt = 'ro')

pyplot.grid(which='both', axis='both')
pyplot.yticks(conteggio, ['/'.join(inv_giocatori1[c[0]]) for c in ordinati])
pyplot.tick_params(axis = 'both', labelsize = 'large')

xN = 2
yN = 30
params = pyplot.gcf()
plSize = params.get_size_inches()
params.set_size_inches( (plSize[0]*xN, plSize[1]*yN) )

pyplot.savefig("test.pdf", format = "pdf")

pyplot.figure(2)

for g in ordinati[-25:]:
    pyplot.plot([(i[0]) for i in mydict2[g[0]]], \
                [(i[1] - 2 * i[2]) for i in mydict2[g[0]]], \
                  '-', \
                  drawstyle = 'steps', \
                  label = '/'.join(inv_giocatori1[g[0]]))

legend = pyplot.legend(loc = 'lower left')
pyplot.tick_params(axis = 'both', labelsize = 'large')
pyplot.savefig("test1.pdf", format = "pdf")
#pyplot.show()
