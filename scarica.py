import mwclient
import csv

site = mwclient.Site('lol.gamepedia.com', path="/")
limite = 500
i = 588
with open('partite2.tsv', 'w', newline='', encoding='utf8') as file:
	writer = csv.writer(file, delimiter="\t", quoting=csv.QUOTE_ALL)
	while True:
		print(i)
		response=site.api('cargoquery',
					limit = limite,
					tables = "ScoreboardGames=SG, ScoreboardPlayers=SP, PlayerRedirects=PR",
					fields = "SG.UniqueGame, SG.DateTime_UTC, SP.PlayerWin, COALESCE(PR.OverviewPage,SP.Link)=N",
					join_on = "SG.UniqueGame=SP.UniqueGame, SP.Link=PR.AllName",
					order_by = "SG.DateTime_UTC, SP.UniqueGame",
					offset = i * limite
		)
		if not response['cargoquery']:
			break

		for partita in response['cargoquery']:
			p = partita['title']
			writer.writerow([p['DateTime UTC'], p['UniqueGame'], p['PlayerWin'], p['N']])

		i = i + 1
