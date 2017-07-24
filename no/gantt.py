import csv
from datetime import datetime
import matplotlib.pyplot as pyplot
from matplotlib.dates import date2num 
import matplotlib

filename='lol pro rank - Foglio1.csv'
periodoprec=''
i=1

with open(filename, 'rt', encoding='utf-8') as f:
    reader = csv.reader(f)
    pyplot.figure(1)
    pyplot.hold(True)

    for row in reader:
        periodo=row[0]+row[1]
        if not periodo == periodoprec:
            inizio=datetime.strptime(row[0],'%d/%m/%Y')
            fine=datetime.strptime(row[1],'%d/%m/%Y')
            pyplot.hlines(i, date2num(inizio),date2num(fine))
            i=i+1
            print(fine-inizio)

        periodoprec=periodo

pyplot.show()
