import csv, json, glob
from trueskill import Rating, rate, setup
from trueskill.backends import available_backends
from datetime import datetime
from collections import defaultdict
from math import floor
from operator import itemgetter
from itertools import chain

if 'mpmath' in available_backends():
    setup(backend='mpmath')

def convris(r):
	if r == "1":
		return [0,1]
	elif r == "2":
		return [1,0]
	else:
		raise ValueError("non esiste il valore")

da_alias_a_nome = {}
partite = []
with open('partite.tsv', 'rt', encoding = 'utf-8-sig', ) as f:
	reader = csv.reader(f, delimiter="\t")
	for riga in reader:
		data = datetime.strptime(riga[0], '%Y-%m-%d %H:%M:%S')
		squadra1 = riga[3].upper().split(",")
		squadra2 = riga[4].upper().split(",")
		try:
			risultati=convris(riga[2])
		except:
			continue
		partite.append((data, risultati, squadra1, squadra2))
		for g in chain(squadra1, squadra2):
			da_alias_a_nome[g] = g.upper()

da_nomi_ad_alias = defaultdict(list)
for a in da_alias_a_nome.keys():
	n = da_alias_a_nome[a]
	da_nomi_ad_alias[n].append(a)

storico = defaultdict(dict)
for a in da_alias_a_nome.keys():
	n = da_alias_a_nome[a]
	if n not in storico:
		storico[n] = {'alias': list(), 'date': defaultdict(list)}

	storico[n]['alias'].append(a)

punteggi = {}
for i in sorted(partite, key=itemgetter(0)):
	giocatori1 = i[2]
	giocatori2 = i[3]
	squadra1 = dict()
	squadra2 = dict()
	for alias1 in giocatori1:
		persona1 = da_alias_a_nome[alias1]
		if not persona1 in punteggi:
			punteggi[persona1] = Rating()

		for alias2 in giocatori2:
			persona2 = da_alias_a_nome[alias2]
			if not persona2 in punteggi:
				punteggi[persona2] = Rating()

			squadra1[persona1] = punteggi[persona1]
			squadra2[persona2] = punteggi[persona2]

	ris1, ris2 = rate([squadra1, squadra2], ranks=i[1])

	t = i[0].date().isoformat()
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
	g.append((r, '/'.join(val['alias'])))

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
