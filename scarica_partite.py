from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import quote
from bs4 import BeautifulSoup

base_sito='http://lol.gamepedia.com'
sito = base_sito + '/Premier_Tournaments'
q = Request(sito)
q.add_header('User-Agent', 'Mozilla/5.0')
tornei = urlopen(q).read()
soup = BeautifulSoup(tornei, 'html5lib')
table = soup.find('table', {'class': 'prettytable sortable'})
tabella = table.find_all('tr')
link = []
for r in tabella:
    try:
        s = r.find_all('td')
        a = s[1].find('a')
        link.append((s[1].text, a['href']))

    except (AttributeError, IndexError, TypeError):
        pass


for l in link[-37::-1]:
    try:
        print(l[0])
        sito = base_sito + l[1]
        q = Request(sito)
        q.add_header('User-Agent', 'Mozilla/5.0')
        torneo = urlopen(q).read()
        soup = BeautifulSoup(torneo, 'html5lib')
        try:
            squadre = soup.find_all('table', {'class' : 'wikitable'})
            for s in squadre:
                nome_sq = s.find('caption')
                print(nome_sq.text)

        except AttributeError:
            raise

    except:
        raise
