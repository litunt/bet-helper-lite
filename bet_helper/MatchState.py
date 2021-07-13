from bet_helper import Score
from datetime import datetime


class MatchState:

    def __init__(self, score: Score, home_team_moneyline: float, away_team_moneyline: float,
                 home_team_spread: tuple, away_team_spread: tuple, under: tuple, over: tuple):
        self.time = datetime.now()
        self.score = score
        self.home_team_moneyline = home_team_moneyline
        self.away_team_moneyline = away_team_moneyline
        self.away_team_spread = away_team_spread
        self.home_team_spread = home_team_spread
        self.under = under
        self.over = over

    def __str__(self):
        return f'Match State: {self.time} \n' \
               f'Score: {self.score} \n' \
               f'Away/Home moneylines: {self.home_team_moneyline}/{self.away_team_moneyline} \n' \
               f'Spread: {self.home_team_spread}/ {self.away_team_spread} \n' \
               f'Over/Under: {self.under}/{self.over}'

    def __eq__(self, other):
        if isinstance(other, MatchState):
            return self.score == other.score and self.away_team_moneyline == other.away_team_moneyline \
                   and self.home_team_moneyline == other.home_team_moneyline \
                   and self.away_team_spread == other.away_team_spread \
                   and self.home_team_spread == other.home_team_spread and self.over == other.over \
                   and self.under == other.under
