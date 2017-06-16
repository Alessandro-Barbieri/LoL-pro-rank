import csv
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError

filename='lol pro rank - Foglio5.csv'
base_sito='http://lol.gamepedia.com/'

with open('giocatori.csv', 'w', newline='',encoding='utf-8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')

    with open(filename, 'rt', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            try:
                sito = base_sito + row[1]
                q=Request(sito)
                q.add_header('User-Agent', 'Mozilla/5.0')
                webpage = urlopen(q).read()

            except HTTPError:
                nome=''
                stato=''

            else:
                soup = BeautifulSoup(webpage, 'html5lib')
                table = soup.find('table', {'class': 'infobox2'})
                th = table.find('th', text=' Name:' + chr(10))
                td = th.findNext('td')
                nome = td.text
                th = table.find('th', text=' Country of Birth:' + chr(10))
                td = th.findNext('td')
                a = td.findNext('a')
                stato=a.text

            print(row[1],nome.strip(),stato)
            spamwriter.writerow([row[1],nome.strip(),stato])
