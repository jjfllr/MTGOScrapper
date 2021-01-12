from time import strptime

import requests
from bs4 import BeautifulSoup


class Deck:
    pilot = ""
    planeswalker = []
    creature = []
    sorcery = []
    instant = []
    artifact = []
    enchantment = []
    land = []
    other = []
    sideboard = []

    def __init__(self):
        self.pilot = ""
        self.planeswalker = []
        self.creature = []
        self.sorcery = []
        self.instant = []
        self.artifact = []
        self.enchantment = []
        self.land = []
        self.other = []
        self.sideboard = []

    def make_deck(self):
        deck = Deck()
        return deck

def get_tournament(fromDate, toDate):
    if not isinstance(fromDate, str) and not isinstance(toDate, str):
        return

    # https://magic.wizards.com/en/section-articles-see-more-ajax
    # ?l=enf
    # &search-result-theme=
    # &limit=6
    # &fromDate=12%2F1%2F2020
    # &toDate=12%2F15%2F2020
    # &sort=DESC
    # &word=modern


    payload = {'l': 'en', 'f': 9041, 'search-result-theme': '', 'limit': 365,
               'fromDate': fromDate, 'toDate': toDate,
               'sort': 'DESC', 'word': 'modern'}
    test = requests.get('https://magic.wizards.com/en/section-articles-see-more-ajax', params=payload).json()

    out = []

    for field in test['data']:
        temp = BeautifulSoup(field, 'html.parser')

        title = temp.find('h3').text.lower().replace(' ', '-')
        YYYY = temp.find_all("span", {"class": "year"})[0].text.strip()
        MM = str(strptime(temp.find_all("span", {"class": "month"})[0].text.strip()[0:3], '%b').tm_mon)
        DD = temp.find_all("span", {"class": "day"})[0].text.strip()

        #out.append(title + "-" + YYYY + "-" + MM + "-" + DD)
        out.append(title + "-{:04d}-{:02d}-{:02d}".format(int(YYYY), int(MM), int(DD)))

    return out

def get_decks_from_Web(URL):
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id="content-detail-page-of-an-article")
    # f = open('C:/Users/jjfll/Desktop/test.html', 'w+')
    # f.write(results.prettify())
    # f.close()

    # decks = results.find_all("div", {"class": "page-width bean_block bean_block_deck_list bean--wiz-content-deck-list clearfix"})

    piles = results.find_all("div", {"class": "deck-list-text"})
    pilots = results.find_all("span", {"class": "deck-meta"})
    decks = []

    for counter, pilot in enumerate(pilots):
        decks.append(Deck())
        decks[counter].pilot = pilot.find('h4').text.split(' ', 1)[0]

        categories = [{"class": "sorted-by-planeswalker clearfix element"},
                      {"class": "sorted-by-creature clearfix element"}, {"class": "sorted-by-sorcery clearfix element"},
                      {"class": "sorted-by-instant clearfix element"},
                      {"class": "sorted-by-enchantment clearfix element"},
                      {"class": "sorted-by-artifact clearfix element"},
                      {"class": "sorted-by-Other clearfix element"}, {"class": "sorted-by-land clearfix element"}
                      ]

        pile = piles[counter].find("div", {"class": "sorted-by-overview-container sortedContainer"})
        sb = piles[counter].find("div", {"class": "sorted-by-sideboard-container clearfix element"})

        for category in categories:
            tmp = pile.find("div", category)

            if isinstance(tmp, type(pile)):  # no es elegante para nada
                number = []
                name = []

                number = tmp.find_all("span", {"class": "card-count"})
                names = tmp.find_all("span", {"class": "card-name"})

                for idx, name in enumerate(names):
                    if category == categories[0]:
                        decks[counter].planeswalker.append((number[idx].text, name.text))
                    if category == categories[1]:
                        decks[counter].creature.append((number[idx].text, name.text))
                    if category == categories[2]:
                        decks[counter].sorcery.append((number[idx].text, name.text))
                    if category == categories[3]:
                        decks[counter].instant.append((number[idx].text, name.text))
                    if category == categories[4]:
                        decks[counter].enchantment.append((number[idx].text, name.text))
                    if category == categories[5]:
                        decks[counter].artifact.append((number[idx].text, name.text))
                    if category == categories[6]:
                        decks[counter].other.append((number[idx].text, name.text))
                    if category == categories[7]:
                        decks[counter].land.append((number[idx].text, name.text))

        if isinstance(sb, type(pile)):  # no es elegante para nada
            number = []
            name = []

            number = sb.find_all("span", {"class": "card-count"})
            names = sb.find_all("span", {"class": "card-name"})

            for idx, name in enumerate(names):
                decks[counter].sideboard.append((number[idx].text, name.text))

    return decks

def write_cards_to_file(file, list):
    if list:
        for item in list:
            file.write('\t\t' + item[0] + ' ' + item[1] + '\n')

def save_decks(decks, directory, name):
    file = open(directory + '/' + name + '.txt', 'w+')

    for deck in decks:
        file.write('Pilot: ' + deck.pilot + '\n')
        file.write('\tDeck:\n')
        write_cards_to_file(file, deck.other)
        write_cards_to_file(file, deck.creature)
        write_cards_to_file(file, deck.planeswalker)
        write_cards_to_file(file, deck.artifact)
        write_cards_to_file(file, deck.enchantment)
        write_cards_to_file(file, deck.instant)
        write_cards_to_file(file, deck.sorcery)
        write_cards_to_file(file, deck.land)
        file.write('\tSideBoard:\n')
        write_cards_to_file(file, deck.sideboard)


        file.write('----------------------------------------\n')



    file.close()

def get_decks_from_file(directory):
    open(directory, 'R')



    return 0

def compare_decks(deck1, deck2):
    return 0
