import csv, json
from datetime import datetime
from collections import defaultdict
from math import floor
from trueskill import Rating, rate, setup, expose
from trueskill.backends import available_backends

EXTRA = True

if 'mpmath' in available_backends():
    setup(backend='mpmath')

giocatori = {}
with open('giocatori.tsv', 'rt', encoding='utf-8-sig') as f:
	reader = csv.reader(f, delimiter="\t")
	for riga in reader:
		giocatore = str.upper(riga[1])
		alias = str.upper(riga[0])
		giocatori[alias] = giocatore
		giocatori[giocatore] = giocatore

storico = {}
partite = {}
with open('partite.tsv', 'rt', encoding='utf-8-sig') as f:
	reader = csv.reader(f, delimiter="\t")
	for riga in reader:
		data = datetime.strptime(riga[0], '%Y-%m-%d %H:%M:%S')
		ide = riga[1]
		nome = riga[3]
		risultato = riga[4]
		squadra1 = riga[5].split(',')
		squadra2 = riga[6].split(',')
		if risultato == "2":
			vincitori = squadra2
			perdenti = squadra1
		elif risultato == "1":
			vincitori = squadra1
			perdenti = squadra2
		else:
			print('ERRORE')

		partite[ide] = {'data': data, 'Yes': vincitori, 'No': perdenti}

n = 0
if EXTRA:
	with open('extra.tsv', 'rt', encoding='utf-8-sig') as f:
		reader = csv.reader(f, delimiter="\t")
		for riga in reader:
			n = n + 1
			data = datetime.strptime(riga[1], '%d/%m/%y')
			ide = "".join([riga[2], data.date().isoformat(), str(n)])
			squadra1 = riga[7:12]
			squadra2 = riga[12:17]
			r1 = riga[5]
			r2 = riga[6]
			if (('0' == r1) and ('1' == r2)):
				vincitori = squadra2
				perdenti = squadra1
			elif (('1' == r1) and ('0' == r2)):
				vincitori = squadra1
				perdenti = squadra2
			else:
				print('ERRORE')

			partite[ide] = {'data': data, 'Yes': vincitori, 'No': perdenti}

for c,v in partite.items():
	vincitori = []
	perdenti = []
	for alias in v['Yes']:
		ALIAS = str.upper(alias)
		if ALIAS not in giocatori.keys():
			giocatori[ALIAS] = ALIAS

		nome = giocatori[ALIAS]
		vincitori.append(nome)
		if nome not in storico:
			storico[nome] = {'date': defaultdict(list)}

	v['Yes'] = vincitori
	for alias in v['No']:
		ALIAS = str.upper(alias)
		if ALIAS not in giocatori.keys():
			giocatori[ALIAS] = ALIAS

		nome = giocatori[ALIAS]
		perdenti.append(nome)
		if nome not in storico:
			storico[nome] = {'date': defaultdict(list)}
			
	v['No'] = perdenti

punteggi = {}
for v in sorted(partite.values(), key=lambda x: x['data']):
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
	ris1, ris2 = rate([squadra1, squadra2], ranks=[1, 2])
	for p1 in ris1.keys():
		s = ris1[p1].sigma
		m = ris1[p1].mu
		r = expose(ris1[p1])
		punteggi[p1] = ris1[p1]
		storico[p1]['date'][t] = {'mi': m, 'sigma': s, 'r': r}

	for p2 in ris2.keys():
		s = ris2[p2].sigma
		m = ris2[p2].mu
		r = expose(ris2[p2])
		punteggi[p2] = ris2[p2]
		storico[p2]['date'][t] = {'mi': m, 'sigma': s, 'r': r}

with open('storico.json', 'w', encoding='utf8') as file:
	json.dump(storico, file, sort_keys=True, indent="\t", ensure_ascii=False)

g = []
for nome, val in storico.items():
	l = sorted(list(val['date'].items()))
	r = l[-1][1]['r']
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
