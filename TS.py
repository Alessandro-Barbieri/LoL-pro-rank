import csv, json
from trueskill import Rating, rate, setup
from trueskill.backends import available_backends
from datetime import datetime
from collections import defaultdict

if 'mpmath' in available_backends():
    setup(backend='mpmath')

da_alias_a_nome = {}
filename = 'lol pro rank - Foglio5.csv'
with open(filename, 'rt', encoding = 'utf-8-sig') as f:
	reader = csv.reader(f)
	for riga in reader:
		da_alias_a_nome[riga[1]] = (riga[2], riga[3])

da_nomi_ad_alias = defaultdict(list)
for a in da_alias_a_nome.keys():
	n = da_alias_a_nome[a][0]
	da_nomi_ad_alias[n].append(a)

storico = defaultdict(dict)
for a in da_alias_a_nome.keys():
	n = da_alias_a_nome[a][0]
	if n not in storico:
		storico[n] = {'alias': list(), 'date': defaultdict(list)}

	storico[n]['alias'].append(a)

def convris(r):
	if r == 0:
		return 1
	elif r == 1:
		return 0
	else:
		raise ValueError("non esiste il valore")

partite = []
filename = 'lol pro rank - Foglio1.csv'
with open(filename, 'rt', encoding = 'utf-8-sig') as f:
	reader = csv.reader(f)
	for riga in reader:
		inizio = datetime.strptime(riga[0], '%d/%m/%Y')
		fine = datetime.strptime(riga[1], '%d/%m/%Y')
		lista1 = riga[7:12]
		lista2 = riga[12:17]
		partite.append(((inizio, fine), int(riga[5]), int(riga[6]), lista1, lista2))

punteggi = {}
for i in partite:
	r1 = convris(i[1])
	r2 = convris(i[2])
	lista1 = i[3]
	lista2 = i[4]
	squadra1 = dict()
	squadra2 = dict()
	for alias1 in lista1:
		persona1 = da_alias_a_nome[alias1][0]
		if not persona1 in punteggi:
			punteggi[persona1] = Rating()

		for alias2 in lista2:
			persona2 = da_alias_a_nome[alias2][0]
			if not persona2 in punteggi:
				punteggi[persona2] = Rating()

			squadra1[persona1] = punteggi[persona1]
			squadra2[persona2] = punteggi[persona2]

	ris1, ris2 = rate([squadra1, squadra2], ranks=[r1, 2])
	t = i[0][0].date().isoformat()
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

with open('giocatori.json', 'w', encoding='utf8') as file:
	json.dump(storico, file, sort_keys = True, indent = "\t", ensure_ascii = False)
