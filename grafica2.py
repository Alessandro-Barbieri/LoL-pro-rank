import json
from operator import itemgetter
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio


with open('giocatori.json', encoding = 'utf-8-sig') as j:
	storico = json.load(j)

g = []
for nome, val in storico.items():
	l = sorted(list(val['date'].items()))
	mi = l[-1][1][0]
	sigma = l[-1][1][1]
	g.append((nome, mi - 2*sigma, mi, 2*sigma))

ordinati = sorted(g, key = itemgetter(1) , reverse = False)

lunghezza = len(ordinati)
conteggio = np.arange(lunghezza)

err = [c[3] for c in ordinati]
#fig = go.Figure(go.Bar(
		#x = [c[2] for c in ordinati],
		#y = conteggio,
		#error_x = dict(type='data', array=err),
		#orientation='h'))

#fig.show()
#pio.orca.config.default_height=lunghezza * 1
#fig.write_image("fig1.png")
#pyplot.axis('tight')
#pyplot.grid(which='both', axis='both')
#pyplot.yticks(conteggio, ['/'.join(storico[c[0]]['alias']) for c in ordinati])
#pyplot.tick_params(axis = 'both')
#pyplot.savefig("test.pdf", format = "pdf", bbox_inches='tight')

#pyplot.figure(2)

#N=50
#xN = 2
#yN = 2
#params = pyplot.gcf()
#plSize = params.get_size_inches()
#params.set_size_inches((plSize[0]*xN, plSize[1]*yN))

fig = go.Figure()

for g in ordinati[-50:]:
	n = g[0]
	l = sorted(list(storico[n]['date'].items()))
	x = [(datetime.strptime(i[0], '%Y-%m-%d')) for i in l]
	y = [(i[1][0] - 2 * i[1][1]) for i in l]
	l = '/'.join(storico[n]['alias'])
	fig.add_trace(go.Scatter(name = l, x = x, y = y))
	#pyplot.plot(x, y, '-', drawstyle = 'steps', label = l)

fig.show()

#legend = pyplot.legend(loc = 'lower left')
#pyplot.tick_params(axis = 'both', labelsize = 'large')
#pyplot.savefig("test1.pdf", bbox_inches='tight', format = "pdf")
