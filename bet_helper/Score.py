class Score:
    def __init__(self, home_team_score: int, away_team_score: int):
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score

    @classmethod
    def create_object(cls, *args):
        # method that allows call multiple constructors
        if isinstance(args[0], str) and len(args) == 1:  # Score.create_object('15:11')
            score = args[0].split(':')
            home_score = int(score[0])
            away_score = int(score[1])
            return cls(home_score, away_score)
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):  # Score.create_object(3, 9)
            home_score = args[0]
            away_score = args[1]
            return cls(home_score, away_score)

    def __eq__(self, other):
        if isinstance(other, Score):
            return self.away_team_score == other.away_team_score and self.home_team_score == other.home_team_score

    def __str__(self):
        # maybe should reverse those parameters -> (home:away)
        return f'({self.home_team_score}:{self.away_team_score})'
