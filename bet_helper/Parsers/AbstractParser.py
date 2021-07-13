from abc import ABC, abstractmethod
from selenium import webdriver

# Used in sub-classes
from bs4 import BeautifulSoup
from bet_helper.MatchState import MatchState
from bet_helper.Score import Score
import time


class AbstractParser(ABC):
    def __init__(self, web_driver: webdriver, updating_frequency=0.0):
        self.is_working = False

        self.web_driver = web_driver
        self.updating_frequency = updating_frequency

    def set_frequency(self, new_frequency: float):
        self.updating_frequency = new_frequency

    def start(self):
        self.is_working = True

    def stop(self):
        self.is_working = False

    @abstractmethod
    def get_team_names(self):
        pass

    @abstractmethod
    def get_game_state(self):
        pass

    def remove_trash_from_list(self, items_to_be_removed: list, list_to_be_cleared: list):
        clear_list = list_to_be_cleared
        for item in items_to_be_removed:
            clear_list = list(filter(item.__ne__, clear_list))
        return clear_list
