import json
import re
from app.parse import letters_to_ascii

crypt_file = open("app/vtescrypt.json", "r")
crypt = json.load(crypt_file)


def parse_discipline_list(discipline_input):
    discipline_list = {}
    for i in discipline_input:
        if i == "abo":
            discipline_list['Abombwe'] = 1
        elif i == "ABO":
            discipline_list['Abombwe'] = 2
        elif i == "ani":
            discipline_list['Animalism'] = 1
        elif i == "ANI":
            discipline_list['Animalism'] = 2
        elif i == "aus":
            discipline_list['Auspex'] = 1
        elif i == "AUS":
            discipline_list['Auspex'] = 2
        elif i == "cel":
            discipline_list['Celerity'] = 1
        elif i == "CEL":
            discipline_list['Celerity'] = 2
        elif i == "chi":
            discipline_list['Chimerstry'] = 1
        elif i == "CHI":
            discipline_list['Chimerstry'] = 2
        elif i == "dai":
            discipline_list['Daimoinon'] = 1
        elif i == "DAI":
            discipline_list['Daimoinon'] = 2
        elif i == "dom":
            discipline_list['Dominate'] = 1
        elif i == "DOM":
            discipline_list['Dominate'] = 2
        elif i == "for":
            discipline_list['Fortitude'] = 1
        elif i == "FOR":
            discipline_list['Fortitude'] = 2
        elif i == "dem":
            discipline_list['Dementation'] = 1
        elif i == "DEM":
            discipline_list['Dementation'] = 2
        elif i == "mel":
            discipline_list['Melpominee'] = 1
        elif i == "MEL":
            discipline_list['Melpominee'] = 2
        elif i == "myt":
            discipline_list['Mytherceria'] = 1
        elif i == "MYT":
            discipline_list['Mytherceria'] = 2
        elif i == "nec":
            discipline_list['Necromancy'] = 1
        elif i == "NEC":
            discipline_list['Necromancy'] = 2
        elif i == "obe":
            discipline_list['Obeah'] = 1
        elif i == "OBE":
            discipline_list['Obeah'] = 2
        elif i == "obf":
            discipline_list['Obfuscate'] = 1
        elif i == "OBF":
            discipline_list['Obfuscate'] = 2
        elif i == "obt":
            discipline_list['Obtenebration'] = 1
        elif i == "OBT":
            discipline_list['Obtenebration'] = 2
        elif i == "pot":
            discipline_list['Potence'] = 1
        elif i == "POT":
            discipline_list['Potence'] = 2
        elif i == "pre":
            discipline_list['Presence'] = 1
        elif i == "PRE":
            discipline_list['Presence'] = 2
        elif i == "pro":
            discipline_list['Protean'] = 1
        elif i == "PRO":
            discipline_list['Protean'] = 2
        elif i == "ser":
            discipline_list['Serpentis'] = 1
        elif i == "SER":
            discipline_list['Serpentis'] = 2
        elif i == "san":
            discipline_list['Sanguinus'] = 1
        elif i == "SAN":
            discipline_list['Sanguinus'] = 2
        elif i == "spi":
            discipline_list['Spiritus'] = 1
        elif i == "SPI":
            discipline_list['Spiritus'] = 2
        elif i == "tem":
            discipline_list['Temporis'] = 1
        elif i == "TEM":
            discipline_list['Temporis'] = 2
        elif i == "thn":
            discipline_list['Thanatosis'] = 1
        elif i == "THN":
            discipline_list['Thanatosis'] = 2
        elif i == "tha":
            discipline_list['Thaumaturgy'] = 1
        elif i == "THA":
            discipline_list['Thaumaturgy'] = 2
        elif i == "qui":
            discipline_list['Quietus'] = 1
        elif i == "QUI":
            discipline_list['Quietus'] = 2
        elif i == "val":
            discipline_list['Valeren'] = 1
        elif i == "VAL":
            discipline_list['Valeren'] = 2
        elif i == "vic":
            discipline_list['Vicissitude'] = 1
        elif i == "VIC":
            discipline_list['Vicissitude'] = 2
        elif i == "vis":
            discipline_list['Visceratika'] = 1
        elif i == "VIS":
            discipline_list['Visceratika'] = 2
        # TODO IMBUED SEARCH BY DIS
        # elif i == "def":
        #     discipline_list.append('Defence')
        # elif i == "inn":
        #     discipline_list.append('Innocence')
        # elif i == "jud":
        #     discipline_list.append('Judgement')
        # elif i == "Mar":
        #     discipline_list.append('Martyrdom')
        # elif i == "red":
        #     discipline_list.append('Redemption')
        # elif i == "ven":
        #     discipline_list.append('Vengeance')
        # elif i == "visi":
        #     discipline_list.append('Vision')
    return discipline_list


def get_overall_crypt(card_lists):
    match_list = card_lists.pop()
    while card_lists:
        pre_match_list = []
        for i in card_lists.pop():
            if i in match_list:
                pre_match_list.append(i)
        match_list = pre_match_list

    return match_list


# Disciplines by text
# def get_crypt_by_discipline(discipline_input):
#     discipline_list = parse_discipline_list(discipline_input)
#     discipline_counter = len(discipline_list)
#     match_cards = []
#     for card in crypt:
#         counter = 0
#         for k, v in discipline_list.items():
#             if k in card:
#                 if card[k] >= v:
#                     counter += 1
#         if discipline_counter == counter:
#             match_cards.append(card)
#     return match_cards


# Disciplines by checkboxes
def get_crypt_by_discipline(discipline_input):
    discipline_list = parse_discipline_list(discipline_input)
    discipline_counter = len(discipline_list)
    match_cards = []
    for card in crypt:
        counter = 0
        for k, v in discipline_list.items():
            if k in card:
                if card[k] >= v:
                    counter += 1
        if discipline_counter == counter:
            match_cards.append(card)
    return match_cards


def get_crypt_by_cardtext(cardtext):
    match_cards = []
    cardtext = cardtext.lower()
    for card in crypt:
        if cardtext in card['Card Text'].lower(
        ) or cardtext in card['Name'].lower():
            match_cards.append(card)
    return match_cards


def get_crypt_by_trait(traits):
    match_cards = []
    for card in crypt:
        for trait in traits:
            if trait == 'enter combat':
                name = re.match(r'^\w+', card['Name'].lower())
                if re.search(
                        r'(he|she|it|they|{}) (can|may)( .* to)? {}'.format(
                            name[0], trait), card['Card Text'].lower()):
                    match_cards.append(card)
            elif trait == 'optional press':
                name = re.match(r'^\w+', card['Name'].lower())
                if re.search(
                        r'(he|she|it|they|{}) gets (.*)?{}'.format(
                            name[0], trait), card['Card Text'].lower()):
                    match_cards.append(card)
            elif re.search(r'{}'.format(trait), card['Card Text'].lower()):
                match_cards.append(card)
    return match_cards


def get_crypt_by_title(title_list):
    match_cards = []
    for card in crypt:
        if card['Title'] in title_list:
            match_cards.append(card)
    return match_cards


def get_crypt_by_votes(votes):
    title_worth = {
        "primogen": 1,
        "prince": 2,
        "justicar": 3,
        "imperator": 3,
        "inner circle": 4,
        "bishop": 1,
        "archbishop": 2,
        "priscus": 3,
        "cardinal": 3,
        "regent": 4,
        "1 vote": 1,
        "2 votes": 2,
        "magaji": 2,
        "kholo": 2,
        "baron": 2
    }
    match_cards = []
    for card in crypt:
        if card['Title'] and votes != 0:
            if title_worth[card['Title']] >= votes:
                match_cards.append(card)
        elif card['Title'] == '' and votes == 0:
            match_cards.append(card)

    return match_cards


def get_crypt_by_capacity(capacity, moreless):
    match_cards = []
    for card in crypt:
        if moreless == '<=':
            if card['Capacity'] <= capacity:
                match_cards.append(card)
        elif moreless == '>=':
            if card['Capacity'] >= capacity:
                match_cards.append(card)
    return match_cards


def get_crypt_by_clan(clan):
    match_cards = []
    for card in crypt:
        if card['Clan'] == clan:
            match_cards.append(card)
    return match_cards


def get_crypt_by_sect(sect):
    match_cards = []
    for card in crypt:
        if re.search(r'^{}[:. $]'.format(sect), card['Card Text']):
            match_cards.append(card)
    return match_cards


def get_crypt_by_group(group_list):
    match_cards = []
    for card in crypt:
        if card['Group'] in group_list or card['Group'] == 'ANY':
            match_cards.append(card)
    return match_cards


def parse_crypt_card(cards):
    parsed_crypt = []
    for card in cards:
        card_parsed = {}
        card_parsed['Discipline'] = []
        card_parsed['Capacity'] = card['Capacity']
        card_parsed['Clan'] = card['Clan']
        card_parsed['Group'] = card['Group']
        card_parsed['Card Text'] = []
        card_parsed['Card Text'] = re.split(': |\n', card['Card Text'])
        card_parsed['Title'] = card['Title']
        dis_list = card['Disciplines'].split()
        for dis in dis_list:
            if dis == dis.lower():
                if card['Type'] == 'Imbued' and dis == 'vis':
                    card_parsed['Discipline'].append(['visi', 25])
                else:
                    card_parsed['Discipline'].append([dis, 25])
            else:
                card_parsed['Discipline'].append([dis.lower() + 's', 27])
        if card['Adv']:
            card_parsed['Name'] = card['Name'] + ' [ADV]'
        else:
            card_parsed['Name'] = card['Name']
        card_parsed['URL Name'] = letters_to_ascii(
            re.sub('[\\W]', '', card_parsed['Name'].lower()))
        card_parsed['URL Clan'] = re.sub('[\\W]', '', card['Clan']).lower()
        card_parsed['Id'] = card['Id']

        parsed_crypt.append(card_parsed)

    return parsed_crypt


def print_crypt_total(cards):
    total = []
    group_counter = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for card in cards:
        if card['Group'] == "ANY":
            for i in range(1, 7):
                group_counter[i] += 1
        else:
            group_counter[int(card['Group'])] += 1
    total.append(len(cards))

    for group, quantity in group_counter.items():
        total.append([group, quantity])
    return total
