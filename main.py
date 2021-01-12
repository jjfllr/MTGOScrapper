# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from time import strptime

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from DeckUtils import *


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    exploring = 0
    testing = 0
    JSON = 1
    if exploring:
        listURL = 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info'

        opts = Options()
        browser = Chrome()
        browser.get(listURL)

        browser.find_element_by_class_name('filters-wrapper-refine').click()
        from_date = browser.find_element_by_id('datepickerFrom')
        to_date = browser.find_element_by_id('datepickerTo')
        from_date.send_keys('12/1/2020')
        to_date.send_keys('12/15/2020')


        search_form = browser.find_element_by_class_name('form-text')
        search_form.send_keys('modern')
        search_button = browser.find_element_by_id("custom-search-submit")
        search_form.submit()

    if testing:
        tourneys = get_tournament("10/01/2020", "01/11/2021")
        print(tourneys)
        print(len(tourneys))

        BaseURL = 'https://magic.wizards.com/en/articles/archive/mtgo-standings/'
        for tourney in tourneys:
            print(tourney)

            decks = get_decks_from_web(BaseURL + tourney)
            save_decks(decks, './Decks', tourney)

    if JSON:
        tourneys = get_tournament("10/01/2020", "01/12/2021")
        print(tourneys)
        print(len(tourneys))

        BaseURL = 'https://magic.wizards.com/en/articles/archive/mtgo-standings/'
        for tourney in tourneys:
            print(tourney)

            decks = get_decks_from_web(BaseURL + tourney)
            save_decks_as_json(decks, './JSON', tourney)

    #get_decks_from_file('./Decks/modern-showcase-challenge-2020-12-06.txt')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
