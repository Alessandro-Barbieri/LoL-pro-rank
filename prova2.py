import csv,glicko2
from datetime import datetime
from operator import itemgetter
from copy import deepcopy
import matplotlib.pyplot as pyplot
from matplotlib.dates import date2num 
import numpy as np
import matplotlib

giocatori = {}
avversari = {}
storico = []
filename='lol pro rank - Foglio1.csv'
periodoprec=''
N=50

with open(filename, 'rt', encoding='utf-8') as f:
    reader = csv.reader(f)

    for row in reader:
        if (not row[17] == ''):
            periodo=row[0]+row[1]
            inizio=datetime.strptime(row[0],'%d/%m/%Y')
            fine=datetime.strptime(row[1],'%d/%m/%Y')

            if (not periodoprec == periodo) and (not periodoprec == ''):
                for gioc in giocatori.keys():
                    if gioc in avversari.keys():
                        giocatori[gioc].update_player(
                            [a[0]for a in avversari[gioc]],
                            [a[1]for a in avversari[gioc]],
                            [a[2]for a in avversari[gioc]])

                    else:
                        giocatori[gioc].did_not_compete()

                storico.append((deepcopy(giocatori),inizio))
                avversari = {}

            
            squadra1=row[17:22]
            squadra2=row[22:37]

            for gioc1 in squadra1:
                if not gioc1 in giocatori:
                    giocatori[gioc1] = glicko2.Player()

                if not gioc1 in avversari:
                    avversari[gioc1] = []
                    
            for gioc2 in squadra2:
                if not gioc2 in giocatori:
                    giocatori[gioc2] = glicko2.Player()

                if not gioc2 in avversari:
                    avversari[gioc2] = []

            for gioc1 in squadra1:
                for gioc2 in squadra2:
                    avversari[gioc1].append((giocatori[gioc2].rating,
                         giocatori[gioc2].rd,
                         int(row[5])))

            for gioc2 in squadra2:
                for gioc1 in squadra1:
                    avversari[gioc2].append((giocatori[gioc1].rating,
                         giocatori[gioc1].rd,
                         int(row[6])))

            periodoprec = periodo
            
        for gioc in giocatori.keys():
            if gioc in avversari.keys():
                giocatori[gioc].update_player(
                    [a[0]for a in avversari[gioc]],[a[1]for a in avversari[gioc]],
                    [a[2]for a in avversari[gioc]])

            else:
                giocatori[gioc].did_not_compete()

        storico.append((deepcopy(giocatori),inizio))
                    
    ordinati = sorted([(g,
                        giocatori[g].rating - 2 * giocatori[g].rd,
                        giocatori[g].rating,
                        2 * giocatori[g].rd) for g in giocatori.keys()],
                      key=itemgetter(1),
                      reverse=False)
    lunghezza=len(ordinati)
    conteggio=np.arange(lunghezza)
    
    pyplot.figure(1)
    assi = pyplot.axes()
    assi.set_xscale("log") 
    pyplot.errorbar(
        [c[2] for c in ordinati],
        conteggio,
        xerr=[c[3] for c in ordinati],
        fmt='ro')
    pyplot.grid(which='both',axis='x')
    pyplot.yticks(conteggio, [c[0] for c in ordinati])
    pyplot.xlim((ordinati[lunghezza - N][1],
                 ordinati[lunghezza-1][2] + ordinati[lunghezza-1][3]))
    pyplot.ylim((lunghezza -N,lunghezza))

    pyplot.savefig("testP.svg", format="svg")

    pyplot.figure(2)
    y={}
    for s in storico:
        for g in s[0].keys():
            if not g in y.keys():
                y[g]=[]
                
            y[g].append((s[0][g].rating,s[0][g].rd,date2num(s[1])))
        
    date=storico[1]

    for g in ordinati[-25:]:
        c=np.arange(len(y[g[0]]))
        pyplot.plot_date([[y[g[0]][i][2]] for i in c],
                      [[y[g[0]][i][0] - 2*y[g[0]][i][1]] for i in c],
                      '-',
                      drawstyle='steps',
                      label=g[0])

    legend=pyplot.legend(loc='lower left')
    pyplot.savefig("testP1.svg", format="svg")
    pyplot.show()

    
