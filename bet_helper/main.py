from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bet_helper.Parsers.AbstractParser import *
from bet_helper.Parsers.MarathonbetParser import *
from bet_helper.Parsers.FonbetParser import *
import time
import traceback
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

marathon_url = 'https://www.marathonbet.ru/su/live/11773589'
fonbet_url = 'https://www.fonbet.kz/live/basketball/63113/28919248'
is_working = True


def create_driver():
    # making selenium webdriver with options(does not close immediately)
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=chrome_options)


def navigate_to_english_version():
    driver.get(fonbet_url)
    time.sleep(random.uniform(1.7, 3.5))

    button = driver.find_element_by_class_name('modal-window__button')
    if button:
        button.click()

    time.sleep(random.uniform(6, 11))
    # TODO: implement some selenium's waiting functions

    lang_menu = driver.find_element_by_class_name('header__lang-set')
    print("CLICK!!")
    lang_menu.click()
    time.sleep(random.uniform(0.3, 1.1))

    eng_button = driver.find_elements_by_class_name('header__lang-item')
    for button in eng_button:
        if button.text == 'English':
            print(button.text)
            time.sleep(random.uniform(0.3, 1.3))
            button.click()
    time.sleep(7)

    if driver.current_url != fonbet_url:
        driver.get(fonbet_url)
    time.sleep(6.44)


if __name__ == '__main__':
    driver = create_driver()

    try:
        if fonbet_url == '':
            print("Enter match full URL:\n")
            fonbet_url = input()
        navigate_to_english_version()
        fonbet_parser = FonbetParser(driver)

        fonbet_parser.get_game_state()

    except Exception:
        traceback.print_exc()
        print("Error close!")
    finally:
        time.sleep(3)
        driver.close()
        driver.quit()
        print("Web-Driver has successfully stopped")
