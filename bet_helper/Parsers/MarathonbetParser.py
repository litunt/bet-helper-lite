from bet_helper.Parsers.AbstractParser import *


class MarathonbetParser(AbstractParser):
    def __init__(self, web_driver: webdriver):
        super().__init__(web_driver)

        self.selection_key = self.find_selection_key()  # is needed for searching elements by attributes

    def get_team_names(self):
        soup = BeautifulSoup(self.web_driver.page_source, 'lxml')

        tag = 'div'
        # class_attributes = 'member-name nowrap' - attribute for prematch
        class_attributes = 'live-today-member-name nowrap'

        try:
            founded_tags = soup.find_all(tag, class_=class_attributes)

            away_team_name = founded_tags[0].text.replace('\n', '')
            home_team_name = founded_tags[1].text.replace('\n', '')
            return home_team_name, away_team_name
        except IndexError:
            class_attributes = 'member-name nowrap'
            founded_tags = soup.find_all(tag, class_=class_attributes)

            away_team_name = founded_tags[0].text.replace('\n', '')
            home_team_name = founded_tags[1].text.replace('\n', '')
            return home_team_name, away_team_name

    def get_game_state(self):
        # creating delay between parsing iterations
        time.sleep(self.updating_frequency)

        soup = BeautifulSoup(self.web_driver.page_source, 'lxml')

        # TODO: throws error if try parse prematch, because it has not attr 'event-description'(this tags holds score in live)
        trash = ['', '\n']
        score_tag = 'td'
        score_attributes = {'class': 'event-description'}
        score = soup.find(score_tag, score_attributes).text
        score = score.replace('\n', '').split(' ')
        score = self.remove_trash_from_list(trash, score)[0]

        # TODO:throws error, if market is suspended. Cause: no <span> tag with 'data-selection-key' attribute.Needs fix
        home_team_selection_key = self.selection_key + '@Match_Winner_Including_All_OT.HB_H'
        home_team_moneyline = soup.find('span', attrs={'data-selection-key': home_team_selection_key}).text

        away_team_selection_key = self.selection_key + '@Match_Winner_Including_All_OT.HB_A'
        away_team_moneyline = soup.find('span', attrs={'data-selection-key': away_team_selection_key}).text

        handicap_tag = 'td'
        handicap_attributes = {'data-market-type': 'HANDICAP'}
        handicaps = soup.find_all(handicap_tag, attrs=handicap_attributes)
        home_team_handicap = None
        away_team_handicap = None
        if len(handicaps) == 2:
            trash = ['', '\n']
            home_team_handicap = handicaps[0].text.split(' ')
            away_team_handicap = handicaps[1].text.split(' ')
            home_team_handicap = (self.remove_trash_from_list(trash, home_team_handicap)[0].strip('()\n'),
                                  self.remove_trash_from_list(trash, home_team_handicap)[1].strip('()\n'))
            away_team_handicap = (self.remove_trash_from_list(trash, away_team_handicap)[0].strip('()\n'),
                                  self.remove_trash_from_list(trash, away_team_handicap)[1].strip('()\n'))

        total_tag = 'td'
        total_attributes = {'data-market-type': 'TOTAL'}
        totals = soup.find_all(total_tag, attrs=total_attributes)
        home_team_total = None
        away_team_total = None
        if len(totals) == 2:
            trash = ['', '\n']
            home_team_total = totals[0].text.split(' ')
            away_team_total = totals[1].text.split(' ')
            home_team_total = (self.remove_trash_from_list(trash, home_team_total)[0].strip('()\n'),
                               self.remove_trash_from_list(trash, home_team_total)[1].strip('()\n'))
            away_team_total = (self.remove_trash_from_list(trash, away_team_total)[0].strip('()\n'),
                               self.remove_trash_from_list(trash, away_team_total)[1].strip('()\n'))

        return MatchState(Score.create_object(score), home_team_moneyline, away_team_moneyline, home_team_handicap,
                          away_team_handicap, home_team_total, away_team_total)

    def find_selection_key(self):
        soup = BeautifulSoup(self.web_driver.page_source, 'lxml')

        tag = 'span'
        class_attributes = 'selection-link active-selection'

        key_attribute = soup.find(tag, class_=class_attributes).get('data-selection-key')
        key = key_attribute.split('@')[0]
        return key
