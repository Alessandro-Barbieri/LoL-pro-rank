import csv
from glicko2 import glicko2
from datetime import datetime
from operator import itemgetter
from copy import deepcopy
import matplotlib.pyplot as pyplot
from matplotlib.dates import date2num 
import numpy as np
import matplotlib

partite = []
periodi = {}
giocatori1 = {}
giocatori = {}
avversari = {}
storico = []
periodoprec = None

filename = 'lol pro rank - Foglio5.csv'
with open(filename, 'rt', encoding = 'utf-8') as f:
    reader = csv.reader(f)

    for riga in reader:
        giocatori1[riga[1]] = (riga[2], riga[3])
        
filename = 'lol pro rank - Foglio1.csv'        
with open(filename, 'rt', encoding = 'utf-8') as f:
    reader = csv.reader(f)

    for riga in reader:
        inizio = datetime.strptime(riga[0], '%d/%m/%Y')
        fine = datetime.strptime(riga[1], '%d/%m/%Y')
        if not (inizio, fine) in periodi.keys():
            periodi[(inizio, fine)] = (fine - inizio)

        squadra1 = riga[7:12]
        squadra2 = riga[12:17]
        partite.append(((inizio, fine), \
                        int(riga[5]), int(riga[6]), \
                        squadra1, squadra2))

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

for i in sorted([(periodomassimo(i[0], periodi), i[1:]) for i in partite], key = itemgetter(0)):
    periodo = i[0]
    if ((not periodoprec == periodo) and (not periodoprec == None)):
        for gioc in giocatori.keys():
            if gioc in avversari.keys():
                giocatori[gioc].update_player(
                    [a[0]for a in avversari[gioc]],
                    [a[1]for a in avversari[gioc]],
                    [a[2]for a in avversari[gioc]])

            else:
                giocatori[gioc].did_not_compete()

        storico.append((deepcopy(giocatori), periodo))
        avversari = {}

    squadra1 = i[1][2]
    squadra2 = i[1][3]

    for alias1 in squadra1:
        persona1 = daGiocatoreAPersona(alias1, giocatori1)
        if not persona1 in giocatori:
            giocatori[persona1] = glicko2.Player()

        if not alias1 in avversari:
            persona1 = daGiocatoreAPersona(alias1, giocatori1)            
            avversari[persona1] = []
            
    for alias2 in squadra2:
        persona2 = daGiocatoreAPersona(alias2, giocatori1)
        if not persona2 in giocatori:
            giocatori[persona2] = glicko2.Player()

        if not alias2 in avversari:
            persona2 = daGiocatoreAPersona(alias2, giocatori1)            
            avversari[persona2] = []

    for alias1 in squadra1:
        persona1 = daGiocatoreAPersona(alias1, giocatori1)        
        for alias2 in squadra2:
            persona2 = daGiocatoreAPersona(alias2, giocatori1)
            avversari[persona1].append((giocatori[persona2].rating,
                                     giocatori[persona2].rd,
                                     i[1][0]))

    for alias2 in squadra2:
        persona2 = daGiocatoreAPersona(alias2, giocatori1)
        for alias1 in squadra1:
            persona1 = daGiocatoreAPersona(alias1, giocatori1)
            avversari[persona2].append((giocatori[persona1].rating,
                                     giocatori[persona1].rd,
                                     i[1][1]))

    periodoprec = periodo
        
    for gioc in giocatori.keys():
        if gioc in avversari.keys():
            giocatori[gioc].update_player([a[0]for a in avversari[gioc]],
                                          [a[1]for a in avversari[gioc]],
                                          [a[2]for a in avversari[gioc]])

        else:
            giocatori[gioc].did_not_compete()

    storico.append((deepcopy(giocatori), periodo))

matplotlib.rc('font', family = 'Unifont')
ordinati = sorted([(g,
                    giocatori[g].rating - 2 * giocatori[g].rd,
                    giocatori[g].rating,
                    2 * giocatori[g].rd)for g in giocatori.keys()],
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
                 4200))#ordinati[lunghezza-1][2] + ordinati[lunghezza-1][3]))
pyplot.savefig("test.svg", format = "svg")

pyplot.figure(2)
y = {}
for s in storico:
    for g in s[0].keys():
        if not g in y.keys():
            y[g] = []
            
        y[g].append((s[0][g].rating, s[0][g].rd, date2num(s[1][1])))
    
date = storico[1]

for g in ordinati[-25:]:
    c = np.arange(len(y[g[0]]))
    pyplot.plot_date([[y[g[0]][i][2]] for i in c],
                  [[y[g[0]][i][0] - 2 * y[g[0]][i][1]] for i in c],
                  '-',
                  drawstyle = 'steps',
                  label = g[0])

legend = pyplot.legend(loc = 'lower left')
pyplot.tick_params(axis = 'both', labelsize = 'large')
pyplot.savefig("test1.svg", format = "svg")
pyplot.show()
