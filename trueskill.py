import csv, json
from skills import Match, Team, LOSE, WIN
from skills.trueskill import TrueSkillGameInfo, FactorGraphTrueSkillCalculator
from datetime import datetime
from collections import defaultdict

alias_giocatori = {}
filename = 'lol pro rank - Foglio5.csv'
with open(filename, 'rt', encoding = 'utf-8-sig') as f:
	reader = csv.reader(f)

	for riga in reader:
		alias_giocatori[riga[1]] = (riga[2], riga[3])

def daGiocatoreAPersona(alias, lista):
	return(lista[alias][0])

storico = defaultdict(dict)

for a in alias_giocatori.keys():
	p = daGiocatoreAPersona(a, alias_giocatori)
	if p not in storico:
		storico[p] = {'alias': list(), 'date': defaultdict(list)}

	storico[p]['alias'].append(a)

def convris(r):
	if r == 0:
		return LOSE
	elif r == 1:
		return WIN
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
		partite.append(((inizio, fine), convris(int(riga[5])), convris(int(riga[6])), lista1, lista2))

giocate = []
giocatori = {}

default = (25, 25/3)
calculator = FactorGraphTrueSkillCalculator()
game_info = TrueSkillGameInfo()

for i in partite:
	lista1 = i[3]
	lista2 = i[4]

	for alias1 in lista1:
		persona1 = daGiocatoreAPersona(alias1, alias_giocatori)
		if not persona1 in giocatori:
			giocatori[persona1] = default

	for alias2 in lista2:
		persona2 = daGiocatoreAPersona(alias2, alias_giocatori)
		if not persona2 in giocatori:
			giocatori[persona2] = default

	squadra1 = dict()
	squadra2 = dict()

	for alias1 in lista1:
		persona1 = daGiocatoreAPersona(alias1, alias_giocatori)
		for alias2 in lista2:
			persona2 = daGiocatoreAPersona(alias2, alias_giocatori)
			squadra1[persona1] = giocatori[persona1]
			squadra2[persona2] = giocatori[persona2]

	SQ1 = Team(squadra1)
	SQ2 = Team(squadra2)
	teams = Match([SQ1, SQ2], [i[1], i[2]])
	new_ratings = calculator.new_ratings(teams, game_info)
	t = i[0][0].date().isoformat()

	for alias1 in lista1:
		persona1 = daGiocatoreAPersona(alias1, alias_giocatori)
		r = new_ratings.rating_by_id(persona1)
		m = r.mean
		s = r.stdev
		giocatori[persona1] = (m, s)
		storico[persona1]['date'][t] = (m, s)

	for alias2 in lista2:
		persona2 = daGiocatoreAPersona(alias2, alias_giocatori)
		m = r.mean
		s = r.stdev
		giocatori[persona2] = (m, s)
		storico[persona2]['date'][t] = (m, s)

with open('giocatori.json', 'w', encoding='utf8') as file:
	json.dump(storico, file, sort_keys = True, indent = "\t", ensure_ascii = False)
