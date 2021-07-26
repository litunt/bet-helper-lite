from bet_helper.MatchState import *
import os
from datetime import datetime


class Logger:

    def __init__(self, home_team_name, away_team_name):
        self.home_team_name = home_team_name
        self.away_team_name = away_team_name
        self.last_game_state = None

        # gets path of running main.py and using it creates a path for log file
        self.file_name = os.getcwd() + '\\Logger\\logs\\' + self.home_team_name + \
                         ' vs ' + self.away_team_name + '.txt'
        self.file_name = self.file_name.replace(' ', '')
        self.f = None

    def receive_game_state(self, game_state: MatchState):
        self.write_to_file(game_state)
        self.last_game_state = game_state

    def start(self):
        self.create_file()

    def create_file(self):
        self.f = open(self.file_name, 'w+', encoding='utf-8')

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        header = f"Home team: {self.home_team_name} \n" \
                 f"Away team: {self.away_team_name} \n" \
                 f"Time: {dt_string} \n"
        self.f.write(header)

    def open_file(self):
        pass

    def write_to_file(self, new_game_state: MatchState):
        if new_game_state != self.last_game_state:
            line_to_write = f"{new_game_state.time}, Sc: {new_game_state.score}, " \
                            f"A/H ml: {new_game_state.home_team_moneyline}/{new_game_state.away_team_moneyline}, " \
                            f"Spr: {new_game_state.home_team_spread}/{new_game_state.away_team_spread}, " \
                            f"Ov/An: {new_game_state.over}/{new_game_state.under}"
            self.f.write(line_to_write + '\n')

    def stop(self):
        self.close_file()

    def close_file(self):
        self.f.close()
