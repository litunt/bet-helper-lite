from bet_helper.Parsers.AbstractParser import *


class FonbetParser(AbstractParser):
    def __init__(self, web_driver: webdriver):
        super().__init__(web_driver)

    def get_team_names(self):
        soup = BeautifulSoup(self.web_driver.page_source, 'lxml')

        table_tag = 'div'
        table_class_attributes = 'ev-score-table__main--16Rvn'
        founded_table = soup.find(table_tag, class_=table_class_attributes)

        team_names_tag = 'span'
        team_names_class_attributes = 'ev-team__name--3zWY8 _live--2gx4G'
        # TODO: sometime returns NoneType
        founded_team_names = founded_table.find_all(team_names_tag, class_=team_names_class_attributes)
        home_team_name = founded_team_names[0].text
        away_team_name = founded_team_names[1].text

        return home_team_name, away_team_name

    def get_game_state(self):
        time.sleep(self.updating_frequency)
        soup = BeautifulSoup(self.web_driver.page_source, 'lxml')

        tag = 'div'
        class_attributes = 'market-group-box--13myO'  # аттрибут для коробок с датой

        founded_tags = soup.find_all(tag, attrs=class_attributes)

        score = None
        home_team_moneyline = None
        away_team_moneyline = None
        home_team_handicap = None
        away_team_handicap = None
        under = None
        over = None

        score_table_tag = 'div'
        score_table_class_attributes = 'ev-score-table--35j-H'
        founded_score_table = soup.find(score_table_tag, class_=score_table_class_attributes)
        score_tag = 'div'
        score_class_attributes = 'ev-score--2aHgg _main--XcabF'
        # TODO:sometimes can be NoneType, approximately bcs score is changing and have another class attribute
        founded_score_tags = founded_score_table.find_all(score_tag, class_=score_class_attributes)
        home_team_score = founded_score_tags[0].text
        # TODO: index error sometimes, dunno why, but apprximately bcs score turns grey color
        away_team_score = founded_score_tags[1].text
        score = Score.create_object(int(home_team_score), int(away_team_score))

        for tag in founded_tags:

            result_text_tag = 'div'
            result_text_attribute = 'text--1Vjli'

            if tag.find(result_text_tag, class_=result_text_attribute) \
                    and tag.find(result_text_tag, class_=result_text_attribute).text == 'Result':
                moneyline_tag = 'div'
                moneyline_class_attributes = 'v---x8Cq'
                moneylines = tag.find_all(moneyline_tag, class_=moneyline_class_attributes)
                home_team_moneyline = moneylines[0].text
                away_team_moneyline = moneylines[1].text

            # TODO: часто выводится больше 1ого гандикапа, выбрать нужный.
            # TODO: eсли больше одного гандикапа на сайте, то путает их местами
            handicap_text_tag = 'div'
            handicap_text_attribute = 'text--1Vjli'
            if tag.find(handicap_text_tag, class_=handicap_text_attribute) \
                    and tag.find(handicap_text_tag, class_=handicap_text_attribute).text == 'Handicap':
                handicap_tag = 'div'
                handicap_class_attribute = 'common-text--V_0fD'
                founded_handicaps = tag.find_all(handicap_tag, handicap_class_attribute)
                handicap_coefficient_tag = 'div'
                handicap_coefficient_class_attribute = 'v---x8Cq _v-only--2MX1l'
                founded_handicap_coefficients = tag.find_all(handicap_coefficient_tag,
                                                             class_=handicap_coefficient_class_attribute)
                home_team_handicap = (
                    founded_handicaps[0].text.split(' ')[1].strip('()\n'), founded_handicap_coefficients[0].text)
                away_team_handicap = (
                    founded_handicaps[1].text.split(' ')[1].strip('()\n'), founded_handicap_coefficients[1].text)

            if tag.find('div', class_='text--1Vjli') and tag.find('div',
                                                                  class_='text--1Vjli').text == 'Total points':

                totals = soup.find_all('div', class_='market-group-box--13myO')
                clean_values_tag_list = []
                for t in totals:
                    if t.find('div', class_='text--1Vjli') and t.find('div',
                                                                      class_='text--1Vjli').text == 'Total points':
                        # total_value_tags = t.find_all('div', class_='row-common--1kY83')
                        # '\xa0'

                        lines = t.find_all('div', class_='row-common--1kY83')
                        total_value_tags = []
                        total_coef_tags = []

                        total = None
                        # parse total value and coeffs related to it
                        if len(lines) == 3:
                            total_value_tags = lines[1].find_all('div',
                                                                 class_='cell-align-wrap--3gwzh _align-left--3sEXl')
                            total_coef_tags = lines[1].find_all('div', class_='v---x8Cq _v-only--2MX1l')
                            total = total_value_tags[0].text.split('\xa0')[1]
                            under = (total, total_coef_tags[0].text)
                            over = (total, total_coef_tags[1].text)

                        else:
                            total_value_tags = lines[0].find_all('div',
                                                                 class_='cell-align-wrap--3gwzh _align-left--3sEXl')
                            total_coef_tags = lines[0].find_all('div',
                                                                class_='v---x8Cq _v-only--2MX1l')
                            if len(total_value_tags) > 1:
                                # TODO: видимо когда 2 тотала(не 3), вырасывает IndexError
                                total = total_value_tags[1].text.split('\xa0')[1]
                                under = (total, total_coef_tags[2].text)
                                over = (total, total_coef_tags[3].text)

                            else:
                                total = total_value_tags[0].text.split('\xa0')[1]
                                under = (total, total_coef_tags[0].text)
                                over = (total, total_coef_tags[1].text)

                        break
        return MatchState(score, float(home_team_moneyline), float(away_team_moneyline), home_team_handicap, away_team_handicap,
                          under, over)
