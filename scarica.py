import mwclient
import csv

site = mwclient.Site('lol.gamepedia.com', path="/", reqs = { 'timeout': 120 })

t = (
	"ScoreboardGames=SG, "
	"ScoreboardPlayers=SPt1, "
	"ScoreboardPlayers=SPj1, "
	"ScoreboardPlayers=SPm1, "
	"ScoreboardPlayers=SPc1, "
	"ScoreboardPlayers=SPs1, "
	"ScoreboardPlayers=SPt2, "
	"ScoreboardPlayers=SPj2, "
	"ScoreboardPlayers=SPm2, "
	"ScoreboardPlayers=SPc2, "
	"ScoreboardPlayers=SPs2, "
	"PlayerRedirects=PRt1, "
	"PlayerRedirects=PRj1, "
	"PlayerRedirects=PRm1, "
	"PlayerRedirects=PRc1, "
	"PlayerRedirects=PRs1, "
	"PlayerRedirects=PRt2, "
	"PlayerRedirects=PRj2, "
	"PlayerRedirects=PRm2, "
	"PlayerRedirects=PRc2, "
	"PlayerRedirects=PRs2"
)
f = (
	"SG.UniqueGame, "
	"SG.DateTime_UTC, "
	"SG.Winner, "
	"PRt1.OverviewPage=PRt1OP, "
	"PRj1.OverviewPage=PRj1OP, "
	"PRm1.OverviewPage=PRm1OP, "
	"PRc1.OverviewPage=PRc1OP, "
	"PRs1.OverviewPage=PRs1OP, "
	"PRt2.OverviewPage=PRt2OP, "
	"PRj2.OverviewPage=PRj2OP, "
	"PRm2.OverviewPage=PRm2OP, "
	"PRc2.OverviewPage=PRc2OP, "
	"PRs2.OverviewPage=PRs2OP"
)
j = (
	"SG.UniqueGame=SPt1.UniqueGame, "
	"SG.UniqueGame=SPj1.UniqueGame, "
	"SG.UniqueGame=SPm1.UniqueGame, "
	"SG.UniqueGame=SPc1.UniqueGame, "
	"SG.UniqueGame=SPs1.UniqueGame, "
	"SG.UniqueGame=SPt2.UniqueGame, "
	"SG.UniqueGame=SPj2.UniqueGame, "
	"SG.UniqueGame=SPm2.UniqueGame, "
	"SG.UniqueGame=SPc2.UniqueGame, "
	"SG.UniqueGame=SPs2.UniqueGame, "
	"SPt1.Link=PRt1.AllName, "
	"SPj1.Link=PRj1.AllName, "
	"SPm1.Link=PRm1.AllName, "
	"SPc1.Link=PRc1.AllName, "
	"SPs1.Link=PRs1.AllName, "
	"SPt2.Link=PRt2.AllName, "
	"SPj2.Link=PRj2.AllName, "
	"SPm2.Link=PRm2.AllName, "
	"SPc2.Link=PRc2.AllName, "
	"SPs2.Link=PRs2.AllName"
)
w = (
	"SPt1.Role_Number=1 AND "
	"SPj1.Role_Number=2 AND "
	"SPm1.Role_Number=3 AND "
	"SPc1.Role_Number=4 AND "
	"SPs1.Role_Number=5 AND "
	"SPt2.Role_Number=1 AND "
	"SPj2.Role_Number=2 AND "
	"SPm2.Role_Number=3 AND "
	"SPc2.Role_Number=4 AND "
	"SPs2.Role_Number=5 AND "
	"SPt1.Team=SG.Team1 AND "
	"SPj1.Team=SG.Team1 AND "
	"SPm1.Team=SG.Team1 AND "
	"SPc1.Team=SG.Team1 AND "
	"SPs1.Team=SG.Team1 AND "
	"SPt2.Team=SG.Team2 AND "
	"SPj2.Team=SG.Team2 AND "
	"SPm2.Team=SG.Team2 AND "
	"SPc2.Team=SG.Team2 AND "
	"SPs2.Team=SG.Team2"
)
limite = 500
i = 0
with open('partite.tsv', 'w', newline='', encoding='utf8') as file:
	writer = csv.writer(file, delimiter="\t", quoting=csv.QUOTE_ALL)
	while True:
		response=site.api('cargoquery', limit = limite, tables = t, fields = f, join_on = j, where = w, order_by = "SG.DateTime_UTC", offset = i * limite)
		if not response['cargoquery']:
			break

		for partita in response['cargoquery']:
			p = partita['title']
			writer.writerow([p['DateTime UTC'], p['UniqueGame'], p['Winner'], p['PRt1OP'], p['PRj1OP'], p['Spm1OP'], p['PRc1OP'], p['PRs1OP'], p['PRt2OP'], p['PRj2OP'], p['PRm2OP'], p['PRc2OP'], p['PRs2OP']])

		i = i + 1
