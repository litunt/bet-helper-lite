from bet_helper.Parsers.AbstractParser import *


class FonbetParser(AbstractParser):
    def __init__(self, web_driver: webdriver):
        super().__init__(web_driver)

    def get_team_names(self):
        pass

    def get_game_state(self):
        soup = BeautifulSoup(self.web_driver.page_source, 'lxml')

        tag = 'div'
        class_attributes = 'market-group-box--13myO'  # аттрибут для коробок с датой

        founded_tags = soup.find_all(tag, attrs=class_attributes)

        home_team_moneyline = None
        away_team_moneyline = None
        home_team_handicap = None
        away_team_handicap = None
        under = None
        over = None
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
                        coeff = None
                        # parse total value and coeffs related to it
                        if len(lines) == 3:
                            total_value_tags = lines[1].find_all('div',
                                                                 class_='cell-align-wrap--3gwzh _align-left--3sEXl')
                            total_coef_tags = lines[1].find_all('div', class_='v---x8Cq _v-only--2MX1l')
                            total = total_value_tags[0].text.split('\xa0')[1]
                            print(total)
                            coeff = (total_coef_tags[0].text, total_coef_tags[1].text)
                            print(coeff)

                        else:
                            total_value_tags = lines[0].find_all('div',
                                                                 class_='cell-align-wrap--3gwzh _align-left--3sEXl')
                            total_coef_tags = lines[0].find_all('div',
                                                                class_='v---x8Cq _v-only--2MX1l')
                            if len(total_value_tags) > 1:
                                total = total_value_tags[1].text.split('\xa0')[1]
                                coeff = (total_coef_tags[2].text, total_coef_tags[3].text)
                            else:
                                total = total_value_tags[0].text.split('\xa0')[1]
                                coeff = (total_coef_tags[0].text, total_coef_tags[1].text)

                            print(total)
                            print(coeff)

                        break

        pass
