from time import strptime

import json
import requests
from bs4 import BeautifulSoup


def make_deck():
    deck = Deck()
    return deck


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

    def print(self):
        print("pilot: " + self.pilot)
        print("Deck:")
        if self.other:
            for item in self.other:
                print("\t" + str(item[0]) + ' ' + item[1])
        if self.creature:
            for item in self.creature:
                print("\t" + str(item[0]) + ' ' + item[1])
        if self.planeswalker:
            for item in self.planeswalker:
                print("\t" + str(item[0]) + ' ' + item[1])
        if self.artifact:
            for item in self.artifact:
                print("\t" + str(item[0]) + ' ' + item[1])
        if self.enchantment:
            for item in self.enchantment:
                print("\t" + str(item[0]) + ' ' + item[1])
        if self.instant:
            for item in self.instant:
                print("\t" + str(item[0]) + ' ' + item[1])
        if self.sorcery:
            for item in self.sorcery:
                print("\t" + str(item[0]) + ' ' + item[1])
        if self.land:
            for item in self.land:
                print("\t" + str(item[0]) + ' ' + item[1])
        print("Sideboard:")
        if self.sideboard:
            for item in self.sideboard:
                print("\t" + str(item[0]) + ' ' + item[1])


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
        yyyy = temp.find_all("span", {"class": "year"})[0].text.strip()
        mm = str(strptime(temp.find_all("span", {"class": "month"})[0].text.strip()[0:3], '%b').tm_mon)
        dd = temp.find_all("span", {"class": "day"})[0].text.strip()

        # out.append(title + "-" + YYYY + "-" + MM + "-" + DD)
        out.append(title + "-{:04d}-{:02d}-{:02d}".format(int(yyyy), int(mm), int(dd)))

    return out


def get_decks_from_web(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id="content-detail-page-of-an-article")

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


def write_cards_to_file(file, pile):
    if pile:
        for item in pile:
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


def save_decks_as_json(decks, directory, name):
    for itx, deck in enumerate(decks):
        file = open(directory + '/' + name + "_" + str(itx + 1) + '_' + deck.pilot + '.json', 'w+')
        file.write("{\"data\":{")
        file.write("\"pilot\":" + "\"" + deck.pilot + "\"" + ",")
        file.write("\"mainboard\":{")
        file.write("\"other\":[")
        write_cards_to_json(file, deck.other)
        file.write("],\"creature\":[")
        write_cards_to_json(file, deck.creature)
        file.write("],\"planeswalker\":[")
        write_cards_to_json(file, deck.planeswalker)
        file.write("],\"artifact\":[")
        write_cards_to_json(file, deck.artifact)
        file.write("],\"enchantment\":[")
        write_cards_to_json(file, deck.enchantment)
        file.write("],\"instant\":[")
        write_cards_to_json(file, deck.instant)
        file.write("],\"sorcery\":[")
        write_cards_to_json(file, deck.sorcery)
        file.write("],\"land\":[")
        write_cards_to_json(file, deck.land)
        file.write("]")  # land close
        file.write("}")  # MainBoard close
        file.write(",\"sideboard\":[")
        write_cards_to_json(file, deck.sideboard)
        file.write("]")  # SideBoard close
        file.write("}")  # data close
        file.write("}")  # JSON close
        file.close()


def write_cards_to_json(file, pile):
    if pile:
        for idx, item in enumerate(pile):
            if idx != 0:
                file.write(',')
            file.write("{\"count\":" + item[0] + ",\"card\":\"" + item[1] + '\"}')
    else:
        file.write("{}")


def get_decks_from_json_file(directory):
    file = open("./JSON/modern-challenge-2021-01-10_1_HouseOfManaMTG.json")
    jdeck = json.loads(file.readline())

    deck = Deck()
    deck.pilot = jdeck['data']['pilot']

    print("\\\'card\\\'")

    for item in jdeck['data']['mainboard']:
        exec("for itx in jdeck[\'data\'][\'mainboard\'][\'" + item + "\']:\n\texec(\"if itx:\\n\\tdeck." + item + ".append([itx[\'count\'], itx[\'card\']])\")")

    for item in jdeck['data']['sideboard']:
        deck.sideboard.append([item['count'], item['card']])

    deck.print()

    return deck
