from bet_helper.MatchState import *


class Logger:

    def __init__(self, home_team_name, away_team_name):
        self.home_team_name = home_team_name
        self.away_team_name = away_team_name
        self.last_state = None

    def receive_game_state(self, game_state: MatchState):
        pass

    def start(self):
        pass

    def create_file(self):
        pass

    def open_file(self):
        pass

    def write_to_file(self):
        pass

    def stop(self):
        self.close_file()

    def close_file(self):
        pass
