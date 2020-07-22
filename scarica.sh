#!/bin/bash

shopt -s expand_aliases

scarica(){
	NOMEFILE=$1
	URI=$3
	MAX=$2
	for (( i=0; i < MAX; ++i )); do 
		wget -O $NOMEFILE$i.csv $URI"&offset="$(( 500*i ))
	done
}

#rm *.csv

# scarica "partite"						94	"https://lol.gamepedia.com/index.php?title=Special:CargoExport&tables=ScoreboardGames&&fields=_pageName%3DPagina%2CTournament%3DTournament%2CTeam1%3DTeam1%2CTeam2%3DTeam2%2CWinTeam%3DWinTeam%2CLossTeam%3DLossTeam%2CDateTime_UTC%3DDateTime+UTC%2CDST%3DDST%2CTeam1Score%3DTeam1Score%2CTeam2Score%3DTeam2Score%2CWinner%3DWinner%2CGamelength%3DGamelength%2CGamelength_Number%3DGamelength+Number%2CTeam1Bans__full%3DTeam1Bans%2CTeam2Bans__full%3DTeam2Bans%2CTeam1Picks__full%3DTeam1Picks%2CTeam2Picks__full%3DTeam2Picks%2CTeam1Names__full%3DTeam1Names%2CTeam2Names__full%3DTeam2Names%2CTeam1Links__full%3DTeam1Links%2CTeam2Links__full%3DTeam2Links%2CTeam1Dragons%3DTeam1Dragons%2CTeam2Dragons%3DTeam2Dragons%2CTeam1Barons%3DTeam1Barons%2CTeam2Barons%3DTeam2Barons%2CTeam1Towers%3DTeam1Towers%2CTeam2Towers%3DTeam2Towers%2CTeam1Gold%3DTeam1Gold%2CTeam2Gold%3DTeam2Gold%2CTeam1Kills%3DTeam1Kills%2CTeam2Kills%3DTeam2Kills%2CTeam1RiftHeralds%3DTeam1RiftHeralds%2CTeam2RiftHeralds%3DTeam2RiftHeralds%2CTeam1Inhibitors%3DTeam1Inhibitors%2CTeam2Inhibitors%3DTeam2Inhibitors%2CPatch%3DPatch%2CMatchHistory%3DMatchHistory%2CVOD%3DVOD%2CN_Page%3DN+Page%2CN_MatchInTab%3DN+MatchInTab%2CN_MatchInPage%3DN+MatchInPage%2CN_GameInMatch%3DN+GameInMatch%2CGamename%3DGamename%2COverviewPage%3DOverviewPage%2CUniqueGame%3DUniqueGame%2CUniqueLine%3DUniqueLine%2CScoreboardID_Wiki%3DScoreboardID+Wiki%2CScoreboardID_Riot%3DScoreboardID+Riot%2CNote1%3DNote1%2CNote2%3DNote2%2CNote3%3DNote3%2CNote4%3DNote4&&order+by=%60cargo__ScoreboardGames%60.%60DateTime_UTC%60&limit=500&format=csv"
 
scarica "giocatori"						27	"https://lol.gamepedia.com/index.php?title=Special:CargoExport&tables=PlayerRedirects&&fields=_pageName%3DPagina%2CAllName%3DAllName%2COverviewPage%3DOverviewPage%2CID%3DID&&order+by=%60_pageName%60%2C%60AllName%60%2C%60OverviewPage%60%2C%60ID%60&limit=500&format=csv"
