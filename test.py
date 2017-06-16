from skills import (
    Match,
    Matches,
    Team,
    WIN,
    LOSE,
    DRAW
    )

from skills.glicko import (
  GlickoCalculator,
  GlickoGameInfo
  )

calculator = GlickoCalculator()
game_info = GlickoGameInfo()
player1 = Team([(1, (1500, 350))])
player2 = Team([(2, (1500, 350))])
player3 = Team([(3, (1500, 350))])
player4 = Team([(4, (1500, 350))])
matches = Matches([Match([player1, player2], [LOSE, WIN]),
                   Match([player1, player3], [WIN, LOSE]),
                   Match([player1, player4], [WIN, LOSE])])
new_ratings = calculator.new_ratings(matches, 1, game_info)

for k in range(1,9):
    print(k,new_ratings.player_rating_by_id(k)[1].mean, \
                                    new_ratings.player_rating_by_id(k)[1].stdev)
