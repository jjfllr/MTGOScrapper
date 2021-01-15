# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from DeckUtils import *


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    if False:
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

    if False:
        tourneys = get_tournament("10/01/2020", "01/11/2021")
        print(tourneys)
        print(len(tourneys))

        BaseURL = 'https://magic.wizards.com/en/articles/archive/mtgo-standings/'
        for tourney in tourneys:
            print(tourney)

            decks = get_decks_from_web(BaseURL + tourney)
            save_decks(decks, './Decks', tourney)

    if True: #test 2
        if False:
            tourneys = get_tournament("10/01/2020", "01/14/2021")

            print(tourneys)

            print(len(tourneys))

            BaseURL = 'https://magic.wizards.com/en/articles/archive/mtgo-standings/'
            for tourney in tourneys:
                print(tourney)

                decks = get_decks_from_web(BaseURL + tourney)
                save_decks_as_json(decks, './JSON', tourney)

        if True:
            decks = []
            if True:
                decks.append(get_deck_from_json_file('./JSON/modern-challenge-2020-10-05_1_Parrit_(1st Place).json'))
                decks.append(get_deck_from_json_file('JSON/modern-challenge-2020-10-05_2_kiko_(2nd Place).json'))
            else:
                decks = get_json_decks_folder('./JSON')

            cummulative_mainboard = [[],[]]

            # create the histogram for the decks
            i = 0
            for deck in decks:
                for idx, card in enumerate(
                        [deck.other, deck.creature, deck.planeswalker, deck.artifact, deck.enchantment, deck.instant,
                         deck.sorcery, deck.land]):
                    if card:
                        for instance in card:
                            if not instance[1] in cummulative_mainboard[1]:
                                cummulative_mainboard[0].append(instance[0])
                                cummulative_mainboard[1].append(instance[1])
                            else:
                                cummulative_mainboard[0][cummulative_mainboard[1].index(instance[1])] += instance[0]

            #cummulative mainboard serves as a hash table for the following operations

            print(cummulative_mainboard)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
