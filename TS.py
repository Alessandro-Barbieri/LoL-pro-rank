import csv, json, glob
from trueskill import Rating, rate, setup
from trueskill.backends import available_backends
from datetime import datetime
from collections import defaultdict, OrderedDict
from math import floor
from operator import itemgetter
from itertools import chain

if 'mpmath' in available_backends():
    setup(backend='mpmath')

storico = defaultdict(dict)
partite = OrderedDict()
with open('partite.tsv', 'rt', encoding = 'utf-8-sig', ) as f:
	reader = csv.reader(f, delimiter="\t")
	for riga in reader:
		data = datetime.strptime(riga[0], '%Y-%m-%d %H:%M:%S')
		id = riga[1]
		nome = riga[3]
		risultato = riga[2]
		if id not in partite.keys():
			partite[id] = {'data': data, 'Yes': list(), 'No': list()}

		#try:
		partite[id][risultato].append(nome)
		#except:
		#	continue
		if nome not in storico:
			storico[nome] = {'date': defaultdict(list)}

punteggi = {}
for k,v in partite.items():
	squadra1 = dict()
	squadra2 = dict()
	vincitori = v['Yes']
	perdenti = v['No']

	for g in vincitori:
		if not g in punteggi.keys():
			punteggi[g] = Rating()

		squadra1[g] = punteggi[g]

	for g in perdenti:
		if not g in punteggi.keys():
			punteggi[g] = Rating()

		squadra2[g] = punteggi[g]

	t = v['data'].date().isoformat()
#	print(t, k)
	ris1, ris2 = rate([squadra1, squadra2], ranks = [1,2])
	for p1 in ris1.keys():
		s = ris1[p1].sigma
		m = ris1[p1].mu
		punteggi[p1] = ris1[p1]
		storico[p1]['date'][t] = (m, s)

	for p2 in ris2.keys():
		s = ris2[p2].sigma
		m = ris2[p2].mu
		punteggi[p2] = ris2[p2]
		storico[p2]['date'][t] = (m, s)

with open('storico.json', 'w', encoding='utf8') as file:
	json.dump(storico, file, sort_keys = True, indent = "\t", ensure_ascii = False)

g = []
for nome, val in storico.items():
	l = sorted(list(val['date'].items()))
	mi = l[-1][1][0]
	sigma = l[-1][1][1]
	r = mi - 2*sigma
	g.append((r, nome))

ordinati = sorted(g, reverse=True)
lista = []
for i in ordinati:
	r = i[0]
	if r <= 0:
		r = 0
	elif r >= 50:
		r = 50
	else:
		r = int(floor(r))
	lista.append((r, i[1]))

with open('risultati.tsv', 'w', newline='', encoding='utf8') as f:
	writer = csv.writer(f, delimiter="\t", quoting=csv.QUOTE_ALL)
	writer.writerows(lista)
