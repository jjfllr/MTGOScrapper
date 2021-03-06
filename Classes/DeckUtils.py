from time import strptime

import os
import json
import requests
from bs4 import BeautifulSoup

from Classes.Rank import Rank, display_title
from Classes.Match import Match
from Classes.Deck import Deck
from Classes.Tournament import Tournament


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
    torunaments = requests.get('https://magic.wizards.com/en/section-articles-see-more-ajax', params=payload).json()

    out = []

    for field in torunaments['data']:
        temp = BeautifulSoup(field, 'html.parser')

        title = temp.find('h3').text.lower().replace(' ', '-')
        yyyy = temp.find_all("span", {"class": "year"})[0].text.strip()
        mm = str(strptime(temp.find_all("span", {"class": "month"})[0].text.strip()[0:3], '%b').tm_mon)
        dd = temp.find_all("span", {"class": "day"})[0].text.strip()

        # out.append(title + "-" + YYYY + "-" + MM + "-" + DD)
        out.append(title + "-{:04d}-{:02d}-{:02d}".format(int(yyyy), int(mm), int(dd)))

    return out


def get_tournament_data_from_web(url):
    tournament = Tournament()

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    result = soup.find(id="content-detail-page-of-an-article")

    # explore tournament
    quarterfinals = result.find_all("div", {"class": "bracket quarterfinals first"})
    semifinals = result.find_all("div", {"class": "bracket semifinals"})
    finals = result.find_all("div", {"class": "finalists"})
    # ranking stored in table with classes odd and even
    table = result.find_all("tr", {"class": "odd"}) + result.find_all("tr", {"class": "even"})

    decks = get_decks_from_web(url)

    for idx, entry in enumerate(table):
        fields = table[idx].find_all("td")

        rank = Rank(int(fields[0].text), fields[1].text, int(fields[2].text), float(fields[3].text), float(fields[4].text), float(fields[5].text))
        tournament.ranking.append(rank)

    tournament.ranking.sort(key=lambda x: Rank.get_rank(x))

    display_title()
    for rank in tournament.ranking:
        rank.display()


def get_decks_from_web(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    return get_deck_from_soup(soup)


def get_deck_from_soup(soup):
    results = soup.find(id="content-detail-page-of-an-article")

    piles = results.find_all("div", {"class": "deck-list-text"})
    pilots = results.find_all("span", {"class": "deck-meta"})

    decks = []

    for counter, pilot in enumerate(pilots):
        decks.append(Deck())
        pilotinfo = pilot.find('h4').text.split(' ', 1)
        if len(pilotinfo) == 2:
            decks[counter].score = pilotinfo[1]
        decks[counter].pilot = pilotinfo[0]

        categories = [
            {"class": "sorted-by-planeswalker clearfix element"},
            {"class": "sorted-by-creature clearfix element"},
            {"class": "sorted-by-sorcery clearfix element"},
            {"class": "sorted-by-instant clearfix element"},
            {"class": "sorted-by-enchantment clearfix element"},
            {"class": "sorted-by-artifact clearfix element"},
            {"class": "sorted-by-Other clearfix element"},
            {"class": "sorted-by-land clearfix element"}
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
                    decks[counter].mainboard.append((number[idx].text, name.text))

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
        file.write('Score: ' + deck.score + '\n')
        file.write('\tDeck:\n')
        write_cards_to_file(file, deck.mainboard)
        file.write('\tSideBoard:\n')
        write_cards_to_file(file, deck.sideboard)
        file.write('----------------------------------------\n')
    file.close()


def save_decks_as_json(decks, directory, name):
    for itx, deck in enumerate(decks):
        file = open(directory + '/' + name + "_" + str(itx + 1) + '_' + deck.pilot + '_' + deck.score + '.json', 'w+')
        file.write("{\n\t\"deck\": {\n")
        file.write("\t\t\"pilot\": " + "\"" + deck.pilot + "\"" + ",\n")
        file.write("\t\t\"score\": " + "\"" + deck.score + "\"" + ",\n")
        file.write("\t\t\"mainboard\":[\n")
        write_cards_to_json(file, deck.mainboard)
        file.write("\n\t\t],\n")  # MainBoard close
        file.write("\t\t\"sideboard\":[\n")
        write_cards_to_json(file, deck.sideboard)
        file.write("\n\t\t]\n")  # SideBoard close
        file.write("\t}\n")  # data close
        file.write("}")  # JSON close
        file.close()


def write_cards_to_json(file, pile):
    if pile:
        for idx, item in enumerate(pile):
            if idx != 0:
                file.write(',\n')
            file.write("\t\t\t{\"count\":" + item[0] + ",\"card\":\"" + item[1] + '\"}')
    else:
        file.write("{}")


def remove_linebreaks(file):
    noLineBreaks = ""
    for line in file:
        strippedLine = line.strip()
        noLineBreaks += strippedLine
    return noLineBreaks


def get_deck_from_json_file(directory):
    file = open(directory)

    jdeck = json.loads(remove_linebreaks(file))

    deck = Deck()
    deck.pilot = jdeck['deck']['pilot']
    deck.score = jdeck['deck']['score']

    for item in jdeck['deck']['mainboard']:
        deck.mainboard.append([item['count'], item['card']])
    for item in jdeck['deck']['sideboard']:
        deck.sideboard.append([item['count'], item['card']])

    return deck


def get_json_decks_folder(directory):
    decks = []
    for subdir, dirs, files in os.walk(directory):
        for idx, file in enumerate(files):
            if file.endswith(".json"):
                decks.append(get_deck_from_json_file(directory + "/" + file))
    return decks
