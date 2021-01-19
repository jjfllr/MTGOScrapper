# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Classes.DeckUtils import *

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
        tourneys = get_tournament("10/01/2020", "01/14/2021")
        print(len(tourneys))

        BaseURL = 'https://magic.wizards.com/en/articles/archive/mtgo-standings/'
        for tourney in tourneys:
            print(tourney)

            decks = get_decks_from_web(BaseURL + tourney)
            save_decks(decks, './Decks', tourney)

    if True:  # test 2
        if False:
            tourneys = get_tournament("10/01/2020", "01/14/2021")

            print(str(len(tourneys)) + " Obtained...\n")

            BaseURL = 'https://magic.wizards.com/en/articles/archive/mtgo-standings/'
            for tourney in tourneys:
                print(tourney)

                decks = get_decks_from_web(BaseURL + tourney)
                save_decks_as_json(decks, './JSON', tourney)

        if False:
            decks = []
            if False:
                decks.append(get_deck_from_json_file('./JSON/modern-challenge-2020-10-05_1_Parrit_(1st Place).json'))
                decks.append(get_deck_from_json_file('JSON/modern-challenge-2020-10-05_2_kiko_(2nd Place).json'))
            else:
                decks = get_json_decks_folder('./JSON')

            cumulative_mainboard = [[], []]

            # create the histogram for the decks
            i = 0
            for deck in decks:
                for idx, card in enumerate(deck.mainboard):
                    """
                    if card:
                        for instance in card:
                            if not instance[1] in cumulative_mainboard[1]:
                                cumulative_mainboard[0].append(instance[0])
                                cumulative_mainboard[1].append(instance[1])
                            else:
                                cumulative_mainboard[0][cumulative_mainboard[1].index(instance[1])] += instance[0]
                    """
            # cumulative mainboard serves as a hash table for the following operations

            print(cummulative_mainboard)

        if True:
            # https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-showcase-challenge-2021-01-17#bracket

            url = 'https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-showcase-challenge-2021-01-17'

            get_tournament_data_from_web(url)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
