import json
import csv
from datetime import datetime
from operator import itemgetter
from copy import deepcopy
import matplotlib.pyplot as pyplot
from matplotlib.dates import date2num
import numpy as np
import matplotlib
from math import sqrt
import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://127.0.0.1:1234')
multicall = xmlrpc.client.MultiCall(s)

giocatori1 = {}
giocatori = {}
filename = 'lol pro rank - Foglio5.csv'
with open(filename, 'rt', encoding = 'utf-8-sig') as f:
    reader = csv.reader(f)

    for riga in reader:
        giocatori1[riga[1]] = (riga[2],riga[3])

partite = []
periodi = {}
filename = 'lol pro rank - Foglio1.csv'
with open(filename, 'rt', encoding = 'utf-8-sig') as f:
    reader = csv.reader(f)

    for riga in reader:
        inizio = datetime.strptime(riga[0], '%d/%m/%Y')
        fine = datetime.strptime(riga[1], '%d/%m/%Y')
        if not (inizio, fine) in periodi.keys():
            periodi[(inizio, fine)] = (fine - inizio)

        lista1 = riga[7:12]
        lista2 = riga[12:17]
        partite.append(((inizio, fine), \
                        int(riga[5]), int(riga[6]), \
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

storico = []
giocate = []
periodoprec = None
for i in sorted([(periodomassimo(i[0], periodi), i[1:]) for i in partite], key = itemgetter(0)):
    periodo = i[0]
#    print(periodo)
    if periodoprec == None:
        inizio = periodo[1]

    p = (periodo[1] - inizio).days

#    if (not periodoprec == periodo) and (not periodoprec == None):

    lista1 = i[1][2]
    lista2 = i[1][3]

    for alias1 in lista1:
        persona1 = daGiocatoreAPersona(alias1, giocatori1)
        if not persona1 in giocatori:
            giocatori[persona1] = None

    for alias2 in lista2:
        persona2 = daGiocatoreAPersona(alias2, giocatori1)
        if not persona2 in giocatori:
            giocatori[persona2] = None

    for alias1 in lista1:
        persona1 = daGiocatoreAPersona(alias1, giocatori1)
        for alias2 in lista2:
            persona2 = daGiocatoreAPersona(alias2, giocatori1)
            if ((i[1][0] == 0) and (i[1][1] == 1)):
                ris = "B"
            elif ((i[1][0] == 1) and (i[1][1] == 0)):
                ris = "W"
            else:
                print(periodo, lista1, lista2)
                raise "I risultati vanno in coppie (0,1) o (1,0)"

            multicall.WHR.create_game(persona2, persona1, ris, p, 0)

    periodoprec = periodo

multicall()
s.WHR.iterate(200)
for g in giocatori.keys():
    giocatori[g] = s.WHR.ratings_for_player(g)

with open('giocatori.json', 'w', encoding='utf8') as file:
    json.dump(giocatori, file, sort_keys = True, indent = 4, ensure_ascii = False)
