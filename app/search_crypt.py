import json
import re
from app.parse import letters_to_ascii

# Card base file. It is JSON (human-readable format) converted from official
# CVS card base available at vekn.com.
# File in this repository have empty disciplines stripped
# (for marginal performance increase) and some typos fixed.
# One day there will be converter for zero-efforts conversion
# of official CVS.
# You definetely want to take a brief look at the JSON file before going deeper
# in the sources.
crypt_file = open("app/vtescrypt.json", "r")
crypt = json.load(crypt_file)


def parse_discipline_list(discipline_input):
    discipline_list = {}
    # Not like it's really necessary, but official CVS card base
    # use this type of discipline values, so we must adjust our entry.
    # The 'i' value is cryptform.disciplines.choices, defined in views.py
    # and is not like rocks-solid.
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

    return discipline_list


def parse_virtue_list(virtue_input):
    virtue_list = []
    # Virtues are not presented same way as Disciplines in card base
    # so we use another list.
    # 'visi' used for Visionary because 'vis' is reserved for Visceratika
    # Could be full name (i.e. Visionary or Visceratika),
    # but I'm lazy to rename discipline icon images
    for i in virtue_input:
        if i == "def":
            virtue_list.append('def')
        elif i == "inn":
            virtue_list.append('inn')
        elif i == "jud":
            virtue_list.append('jud')
        elif i == "Mar":
            virtue_list.append('mar')
        elif i == "red":
            virtue_list.append('red')
        elif i == "ven":
            virtue_list.append('ven')
        elif i == "visi":
            virtue_list.append('vis')

    return virtue_list


def get_overall_crypt(card_lists):
    match_list = card_lists.pop()
    # 'card-lists' are nested list with all cards matching each of the filters
    # Below we step-by-step compare if next filter cards are in previous
    # list of matching cards (with all previous filters applied), so in the end
    # only cards matching ALL filters are left
    while card_lists:
        pre_match_list = []
        for i in card_lists.pop():
            if i in match_list:
                pre_match_list.append(i)

        match_list = pre_match_list

    return match_list


def get_crypt_by_discipline(discipline_input):
    # List of required disciplies parsed to database format
    discipline_list = parse_discipline_list(discipline_input)
    # Quantity of required disciplines
    discipline_counter = len(discipline_list)
    match_cards = []
    for card in crypt:
        counter = 0
        # Each crypt card is tested if each of its discipline value is
        # more-or-less than required discipline value. Each time it passes
        # counter increments.
        for k, v in discipline_list.items():
            if k in card:
                if card[k] >= v:
                    counter += 1

        # If counter of required disciplines match card discipline counter
        # card is considered OK
        if discipline_counter == counter:
            match_cards.append(card)

    return match_cards


def get_crypt_by_virtues(virtue_input):
    # Same approach as with disciplines but more simple
    match_cards = []
    virtue_list = parse_virtue_list(virtue_input)
    virtue_counter = len(virtue_list)
    for card in crypt:
        if card['Type'] == 'Imbued':
            counter = 0
            disciplines = card['Disciplines'].split()
            for i in virtue_list:
                if i in disciplines:
                    counter += 1

            if virtue_counter == counter:
                match_cards.append(card)

    return match_cards


def get_crypt_by_cardtext(cardtext):
    match_cards = []
    cardtext = cardtext.lower()
    # Search in card name or text, lower-case for simplicity
    for card in crypt:
        if cardtext in card['Card Text'].lower(
        ) or cardtext in card['Name'].lower():
            match_cards.append(card)

    return match_cards


def get_crypt_by_trait(traits):
    match_cards = []
    trait_counter = len(traits)
    for card in crypt:
        counter = 0
        # Below are just dirty hacks to match by 'trait' (card text part).
        # It can break anytime (if card text in CVS card base changes), but
        # just works for now. Please refer to Python Regexp's ('re' module).
        for trait in traits:
            if trait == 'enter combat':
                name = re.match(r'^\w+', card['Name'].lower())
                if re.search(
                        r'(he|she|it|they|{}) (can|may)( .* to)? {}'.format(
                            name[0], trait), card['Card Text'].lower()):
                    counter += 1

            elif trait == 'optional press':
                name = re.match(r'^\w+', card['Name'].lower())
                if re.search(
                        r'(he|she|it|they|{}) gets (.*)?{}'.format(
                            name[0], trait), card['Card Text'].lower()):
                    counter += 1

            elif trait == '[:.] \+1 bleed.':
                if re.search(r'{}'.format('[:.] \+. bleed.'),
                             card['Card Text'].lower()):
                    counter += 1

            elif trait == '[:.] \+1 strength.':
                if re.search(r'{}'.format('[:.] \+. strength.'),
                             card['Card Text'].lower()):
                    counter += 1

            elif re.search(r'{}'.format(trait), card['Card Text'].lower()):
                counter += 1

        if trait_counter == counter:
            match_cards.append(card)

    return match_cards


def get_crypt_by_title(title_list):
    # Title filter is cummulative i.e. it matches cards matching any
    # chosen title form field
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
        # Match cards with any title worth more than required total votes
        if card['Title'] and votes != 0:
            if title_worth[card['Title']] >= votes:
                match_cards.append(card)

        # Match non-titled card
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
        # Imbue 'sect' is defined by card['Type'], others are just 'vampire'
        if sect == 'Imbued' and card['Type'] == sect:
            match_cards.append(card)
            continue

        # For vampires sect is determined only by card['Text']
        # It is another dirty hack (see trait above), but...
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
    # Below we parse each card output from original database format to what
    # is will be showed to user. Everything below in card_parsed goes to
    # templates/html, where it is parsed by jinja2 before it reaches browser.
    for card in cards:
        card_parsed = {}
        card_parsed['Discipline'] = []
        card_parsed['Capacity'] = card['Capacity']
        card_parsed['Clan'] = card['Clan']
        # Just because X is shorter than 'ANY' and we substitute it for output
        if card['Group'] == 'ANY':
            card_parsed['Group'] = 'X'
        else:
            card_parsed['Group'] = card['Group']
        card_parsed['Type'] = card['Type']
        card_parsed['Card Text'] = []
        # Dirty hack to separate card text 'bold' part (sect, title, etc)
        # from main card text
        card_parsed['Card Text'] = re.split(': |\n', card['Card Text'])
        card_parsed['Title'] = card['Title']
        dis_list = card['Disciplines'].split()
        for dis in dis_list:
            # Basic disciplines icons are square so we pass smaller size (24),
            # it is later used in html template
            if dis == dis.lower():
                if card['Type'] == 'Imbued' and dis == 'vis':
                    card_parsed['Discipline'].append(['visi', 24])
                else:
                    card_parsed['Discipline'].append([dis, 24])
            # Superior disciplines icons are diamond so we pass bigger size (27),
            # it is later used in html template. Will start to pass
            # html class one day...
            # 's' added because superior icons are like 'doms.gif'
            # 'dom.gif' for basic Dominate, etc.
            else:
                card_parsed['Discipline'].append([dis.lower() + 's', 27])

        if card['Adv']:
            card_parsed['Name'] = card['Name'] + ' [ADV]'
        else:
            card_parsed['Name'] = card['Name']

        # Card names can be of any unicode letters, but ascii required for
        # image file name in static/img/*. 'URL Name' used only as file name.
        card_parsed['URL Name'] = letters_to_ascii(
            re.sub('[\\W]', '', card_parsed['Name'].lower()))
        # Same as with 'URL Name'
        card_parsed['URL Clan'] = re.sub('[\\W]', '', card['Clan']).lower()
        # Id used to unfold card text in result output
        card_parsed['Id'] = card['Id']

        parsed_crypt.append(card_parsed)

    return parsed_crypt


def print_crypt_total(cards):
    total = []
    # Initial group counters are 0 for all groups, we increment it later
    # for each card matching target group
    group_counter = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for card in cards:
        if card['Group'] == "ANY":
            # For cards with ANY group (e.g. Anarch Convert) increment
            # all group counters
            for i in range(1, 7):
                group_counter[i] += 1
        else:
            group_counter[int(card['Group'])] += 1

    # total[0] to be total quantity of all matching cards
    total.append(len(cards))

    # total[x] to be total quantity of matching cards of particular [x] group
    for group, quantity in group_counter.items():
        total.append([group, quantity])

    return total
