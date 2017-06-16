#import cProfile
import csv
from skills import Match, Matches, Team, WIN, LOSE
from skills.glicko import GlickoCalculator, GlickoGameInfo
from datetime import datetime
from operator import itemgetter
from copy import deepcopy
import matplotlib.pyplot as pyplot
from matplotlib.dates import date2num 
import numpy as np
import matplotlib
from math import sqrt

giocatori1 = {}
giocatori = {}
filename = 'lol pro rank - Foglio5.csv'
with open(filename, 'rt', encoding = 'utf-8') as f:
    reader = csv.reader(f)

    for riga in reader:
        giocatori1[riga[1]] = (riga[2],riga[3])

def convris(r):
    if r == 0:
        return LOSE
    elif r == 1:
        return WIN
    else:
        raise ValueError("non esiste il valore")

partite = []
periodi = {}
filename = 'lol pro rank - Foglio1.csv'        
with open(filename, 'rt', encoding = 'utf-8') as f:
    reader = csv.reader(f)

    for riga in reader:
        inizio = datetime.strptime(riga[0], '%d/%m/%Y')
        fine = datetime.strptime(riga[1], '%d/%m/%Y')
        if not (inizio, fine) in periodi.keys():
            periodi[(inizio, fine)] = (fine - inizio)

        lista1 = riga[7:12]
        lista2 = riga[12:17]
        partite.append(((inizio, fine), \
                        convris(int(riga[5])), convris(int(riga[6])), \
                        lista1, lista2))

for i in deepcopy(periodi).keys():
    for j in deepcopy(periodi).keys():
        if ((i[0] <= j[0] < i[1]) and (i[1] < j[1])):
            periodi[(i[0], j[1])] =  (j[1] - i[0])

        elif ((i[0] < j[1] <= i[1]) and (j[0] < i[0])):
            periodi[(j[0], i[1])] = (i[1] - j[0])

def inclusione(j, per):
    risultato = []
    for i in per.keys():
        if not ((i[0] == j[0] == j[1]) or (i[1] == j[0] == j[1])):
            if ((i[0] <= j[0] <= i[1]) and (i[0] <= j[1] <= i[1])):
                risultato.append(i)

    return risultato

def periodomassimo(i, per):
    inc = inclusione(i, periodi)
    if not inc == []:
        ord = sorted([((e[0], e[1]), e[1] - e[0]) for e in inc], \
                     key = itemgetter(1),reverse = True)
        return(ord[0][0])
    else:
        return(i)

def daGiocatoreAPersona(alias, lista):
    return(lista[alias][0])

calculator = GlickoCalculator(sqrt((350 * 200 - 50 * 50) / 365))

storico = []
giocate = []
periodoprec = None
for i in sorted([(periodomassimo(i[0], periodi), i[1:]) for i in partite], \
                key = itemgetter(0)):
    
    periodo = i[0]
    if periodoprec == None:
        inizio = periodo[1]

    if (not periodoprec == periodo) and (not periodoprec == None):
        GIOC = Matches(giocate)
        game_info = GlickoGameInfo()
        p = (periodo[1] - inizio).days
        if (periodo[1] == periodo[0]):
                p = p + 0.5
                
        new_ratings = calculator.new_ratings(GIOC, p, game_info)

        for k in deepcopy(giocatori).keys():
            try:
                t = new_ratings.player_rating_by_id(k)[1]
                giocatori[k] = (t.mean, t.stdev, t.last_rating_period)
            except TypeError:
                pass
        giocate = []
        storico.append((deepcopy(giocatori), periodo))

    game_info = GlickoGameInfo()

    squadra1 = []#{}
    squadra2 = []#{}
    lista1 = i[1][2]
    lista2 = i[1][3]

    for alias1 in lista1:
        persona1 = daGiocatoreAPersona(alias1, giocatori1)
        if not persona1 in giocatori:
            giocatori[persona1] = (1500, 200)

    for alias2 in lista2:
        persona2 = daGiocatoreAPersona(alias2, giocatori1)
        if not persona2 in giocatori:
            giocatori[persona2] = (1500, 200)

    for alias1 in lista1:
        persona1 = daGiocatoreAPersona(alias1, giocatori1)
        for alias2 in lista2:
            persona2 = daGiocatoreAPersona(alias2, giocatori1)
            SQ1 = Team([(persona1, giocatori[persona1])])
            SQ2 = Team([(persona2, giocatori[persona2])])
            giocate.append(deepcopy(Match([SQ1, SQ2], [i[1][0], i[1][1]])))

##    for alias2 in lista2:
##        persona2 = daGiocatoreAPersona(alias2, giocatori1)
##        for alias1 in lista1:
##            persona1 = daGiocatoreAPersona(alias1, giocatori1)
##            SQ2 = Team([(persona1, giocatori[persona1])])
##            SQ1 = Team([(persona2, giocatori[persona2])])
##            giocate.append(deepcopy(Match([SQ1, SQ2], [i[1][1], i[1][0]])))

    periodoprec = periodo
    
matplotlib.rc('font', family = 'Unifont')
ordinati = sorted([(g,
                    giocatori[g][0] - 2 * giocatori[g][1],
                    giocatori[g][0],
                    2 * giocatori[g][1])for g in giocatori.keys()],
                  key = itemgetter(1),
                  reverse = False)

lunghezza = len(ordinati)
conteggio = np.arange(lunghezza)

N=50
pyplot.figure(1)
pyplot.errorbar([c[2] for c in ordinati],
             conteggio,
             xerr = [c[3] for c in ordinati],
             fmt = 'ro')
pyplot.grid(which='both',axis='x')
pyplot.yticks(conteggio, [c[0] for c in ordinati])
pyplot.tick_params(axis = 'both', labelsize = 'large')
pyplot.ylim((lunghezza - N, lunghezza))
pyplot.xlim((ordinati[lunghezza - N][1],
                 ordinati[lunghezza-1][2] + ordinati[lunghezza-1][3]))
pyplot.savefig("test.svg", format = "svg")

pyplot.figure(2)
y = {}

for s in storico:
    for g in s[0].keys():
        if not g in y.keys():
            y[g] = []

        t = s[0][g]
        y[g].append((t[0], t[1], date2num(s[1][1])))

date = storico[1]

for g in ordinati[-25:]:
    c = np.arange(len(y[g[0]]))
    pyplot.plot_date([[y[g[0]][i][2]] for i in c], \
                     [[y[g[0]][i][0] - 2 * y[g[0]][i][1]] for i in c], \
                     '-', \
                     drawstyle = 'steps', \
                     label = g[0])

legend = pyplot.legend(loc = 'lower left')
pyplot.tick_params(axis = 'both', labelsize = 'large')
pyplot.savefig("test1.svg", format = "svg")
pyplot.show()
