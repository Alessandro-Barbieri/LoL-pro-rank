import mwclient
import csv

site = mwclient.Site('lol.gamepedia.com', path="/")
limite = 500
i=0
with open('giocatori.tsv', 'w', newline='', encoding='utf8') as file:
	writer = csv.writer(file, delimiter="\t", quoting=csv.QUOTE_ALL)
	while True:
		print(i)
		response=site.api('cargoquery',
					limit = limite,
					tables = "PlayerRedirects=PR",
					fields = "PR.AllName, PR.OverviewPage",
					offset = i * limite
		)
		if not response['cargoquery']:
			break

		for partita in response['cargoquery']:
			p = partita['title']
			writer.writerow([p['AllName'], p['OverviewPage']])

		i = i + 1

i = 0
with open('partite.tsv', 'w', newline='', encoding='utf8') as file:
	writer = csv.writer(file, delimiter="\t", quoting=csv.QUOTE_ALL)
	while True:
		print(i)
		response=site.api('cargoquery',
					limit = limite,
					tables = "ScoreboardGames=SG",
					fields = "SG.UniqueGame, SG.DateTime_UTC, SG.Team1, SG.Team2, SG.Winner, SG.Team1Links, SG.Team2Links",
					order_by = "SG.DateTime_UTC",
					offset = i * limite
		)
		if not response['cargoquery']:
			break

		for partita in response['cargoquery']:
			p = partita['title']
			writer.writerow([p['DateTime UTC'], p['UniqueGame'], p['Team1'], p['Team2'], p['Winner'], p['Team1Links'], p['Team2Links']])

		i = i + 1
