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
library_file = open("app/vteslib.json", "r")
library = json.load(library_file)


def get_library_by_cardtext(cardtext):
    match_cards = []
    cardtext = cardtext.lower()
    for card in library:
        if cardtext in card['Card Text'].lower(
        ) or cardtext in card['Name'].lower():
            match_cards.append(card)

    return match_cards


def get_library_by_cardtype(cardtype):
    match_cards = []
    for card in library:
        if cardtype in card['Type'].split('/'):
            match_cards.append(card)

    return match_cards


def get_library_by_discipline(discipline):
    match_cards = []
    for card in library:
        if discipline in card['Discipline']:
            match_cards.append(card)

    return match_cards


def get_library_by_clan(clan):
    match_cards = []
    for card in library:
        if clan == card['Clan']:
            match_cards.append(card)

    return match_cards


def get_library_by_title(title):
    match_cards = []
    for card in library:
        if title in card['Requirement'].lower():
            match_cards.append(card)

    return match_cards


def get_library_by_sect(sect):
    match_cards = []
    for card in library:
        if sect in card['Requirement'].lower():
            match_cards.append(card)

    return match_cards


def get_library_by_blood(cost, moreless):
    match_cards = []
    for card in library:
        if moreless == '<=':
            if card['Blood Cost'] <= cost:
                match_cards.append(card)

        elif moreless == '>=':
            if card['Blood Cost'] >= cost:
                match_cards.append(card)

    return match_cards


def get_library_by_pool(cost, moreless):
    match_cards = []
    for card in library:
        if moreless == '<=':
            if card['Pool Cost'] <= cost:
                match_cards.append(card)

        elif moreless == '>=':
            if card['Pool Cost'] >= cost:
                match_cards.append(card)

    return match_cards


def get_library_by_trait(traits):
    match_cards = []
    for card in library:
        for trait in traits:
            if re.search(r'{}'.format(trait), card['Card Text'].lower()):
                match_cards.append(card)

    return match_cards


def get_overall_library(card_lists):
    # 'card-lists' are nested list with all cards matching each of the filters
    # Below we step-by-step compare if next filter cards are in previous
    # list of matching cards (with all previous filters applied), so in the end
    # only cards matching ALL filters are left
    match_list = card_lists.pop()
    while card_lists:
        pre_match_list = []
        for i in card_lists.pop():
            if i in match_list:
                pre_match_list.append(i)

        match_list = pre_match_list

    return match_list


def parse_library_card(cards):
    # Below we parse each card output from original database format to what
    # is will be showed to user. Everything below in card_parsed goes to
    # templates/html, where it is parsed by jinja2 before it reaches browser.
    parsed_library = []
    for card in cards:
        card_parsed = {}
        card_parsed['Name'] = card['Name']
        card_parsed['Type'] = card['Type']

        if card['Discipline']:
            # Split string from card['Discipline'] into list, required for
            # double (X & Y)/ triple disciplines (anarch, X / Y / Z)
            card_parsed['Discipline'] = re.split('/| & ', card['Discipline'])

            # Discipline icon files named as ---.gif, so we cut discipline name
            card_parsed['URL Discipline'] = []
            for discipline in card_parsed['Discipline']:
                # Hack around Thanatosis and Thaumaturgy
                if discipline == 'Thanatosis':
                    card_parsed['URL Discipline'].append('thn')
                    # Hack around Visionary and Visceratika
                elif discipline == 'Vision':
                    card_parsed['URL Discipline'].append('visi')
                else:
                    card_parsed['URL Discipline'].append(
                        str(discipline[:3].lower()))

            if '/' in card['Discipline']:
                # Insert delimiter for triple disciplines (anarch, X / Y / Z)
                # and double disciplines
                if len(card['Discipline'].split('/')) == 3:
                    card_parsed['URL Discipline'].insert(2, '/')

                card_parsed['URL Discipline'].insert(1, '/')

            if '&' in card['Discipline']:
                # Insert delimiter for double (X & Y) disciplines
                card_parsed['URL Discipline'].insert(1, '+')

        if card['Type'] == 'Ally' or card['Type'] == "Retainer":
            # Not used at the moment, was tested before to show life as
            # icons in card output. It clog interface with doubtful usefulness
            life = re.match(r'.*with ([0-9]) life', card['Card Text'])
            card_parsed['Life'] = life.group(1)

        if card['Type'] == 'Ally':
            # Not used at the moment, was tested before to show strength as
            # icons in card output. It clog interface with doubtful usefulness
            strength = re.match(r'.*([0-9]) strength', card['Card Text'])
            card_parsed['Strength'] = strength.group(1)

        if card['Clan']:
            card_parsed['URL Clan'] = []
            # Used for double clan requirements, e.g. Malkavian/!Maklavian
            # Tremere/!Tremere, etc.
            clan_list = card['Clan'].split('/')
            for clan in clan_list:
                card_parsed['URL Clan'].append(
                    re.sub('[\\W]', '', clan.lower()))

            # Insert delimiter for double (X / Y) clan requirements
            if '/' in card['Clan']:
                card_parsed['URL Clan'].insert(1, '/')

        card_parsed['Card Text'] = card['Card Text'].split('\n')

        card_text_head_keywords = [
            # That is what we use as regexp to determine header text (bold)
            'unique',
            'weapon\.',
            'vehicle\.',
            'equipment\.',
            'electronic\.',
            'requires a',
            'requires the',
            'gehenna\.',
            'event\.',
            'inquisition\.',
            'government\.',
            'inconnu\.',
            'transient\.',
            'out-of-turn',
            'master\.',
            'master:',
            'trifle\.',
            'archetype\.',
            'location\.',
            'discipline\.',
            '^(\+?\w)? (\w+)? action.',
            'only usable \w',
            'do not replace',
            'ammo\.',
            'aim\.',
            '\w+ with \w+ life',
            'boon\.',
            'title\.',
            'only one'
        ]

        for keyword in card_text_head_keywords:
            # First entry of card text is tested for keywords and for mathes
            # 'Card Title Text' will be used later in html template to be bolded
            if re.match(r'(?!^\[).*{}'.format(keyword),
                        card_parsed['Card Text'][0].lower()):
                card_parsed['Card Title Text'] = card_parsed['Card Text'].pop(
                    0)
                break

        card_parsed['Card Middle Text'] = []
        card_parsed['Card Other Text'] = []

        for i in card_parsed['Card Text']:
            # Below we parse main card text to find disciplines/types and append
            # them to 'Card Middle Text' list so it can be parsed later in html
            # template to show disciplines/types images in card text output.
            if re.match(r'(\[+.*?\]+)', i):
                # We expect not more that 3 disciplines/types for iconization
                # for each card.
                # We look for such entries as [an entry] and
                # define it to object 't' (t.group(2) = second match).
                t = re.match(r'(\[.*?\])\s?(\[.*?\])?\s?(\[.*?\])?\s?(.*)', i)
                dis = ''
                dis2 = ''
                dis3 = ''
                # Assign non-discipline (cardtype) list of what must be iconizes
                # First entry is text in ['Card Text']
                # Second entry is image file name (e.g. 'fli'.gif) used in html
                # template later.
                img_list = [('[FLIGHT]', 'fli'), ('[ACTION]', 'act'),
                            ('[ACTION MODIFIER]', 'mod'),
                            ('[REACTION]', 'rea'), ('[REFLEX]', 'ref'),
                            ('[COMBAT]', 'com'), ('[COMBAT]', 'com'),
                            ('[1 CONVICTION]', 'con1'),
                            ('[2 CONVICTION]', 'con2')]

                i = 0
                for i in range(0, len(img_list)):
                    # Test if any keywords from 'img_list' are in card text
                    # match, if so assign it do disX variable
                    if img_list[i][0] == t.group(1):
                        dis = img_list[i][1]
                    elif img_list[i][0] == t.group(2):
                        dis2 = img_list[i][1]
                    elif img_list[i][0] == t.group(3):
                        dis3 = img_list[i][1]

                    if i == len(img_list) - 1:
                        # At last iteration if nothing match img_list,
                        # just assign anything inside [...] to disX
                        # (and remove '[' and ']')
                        if not dis and t.group(1):
                            a = t.group(1).replace('[', '')
                            dis = a.replace(']', '')

                        if not dis2 and t.group(2):
                            a = t.group(2).replace('[', '')
                            dis2 = a.replace(']', '')

                        if not dis3 and t.group(3):
                            a = t.group(3).replace('[', '')
                            dis3 = a.replace(']', '')

                # Create correct middle text order for html template.
                # test for == x.lower() determine if it is superior
                # discipline or basic. For superior we add 's' as card
                # image file name differ from basic by it
                # (e.g. dom.gif vs doms.gif for Basic vs Superior Dominate).
                if dis3:
                    if dis == dis.lower():
                        card_parsed['Card Middle Text'].append(
                            [dis, dis2, dis3, t.group(4)])
                    elif dis2 == dis2.lower():
                        card_parsed['Card Middle Text'].append(
                            [dis.lower() + 's', dis2, dis3,
                             t.group(4)])
                    else:
                        card_parsed['Card Middle Text'].append([
                            dis.lower() + 's',
                            dis2.lower() + 's', dis3,
                            t.group(4)
                        ])
                elif dis2:
                    if dis == dis.lower():
                        card_parsed['Card Middle Text'].append(
                            [dis, dis2, t.group(4)])
                    elif dis2 == dis2.lower():
                        card_parsed['Card Middle Text'].append(
                            [dis.lower() + 's', dis2,
                             t.group(4)])
                    else:
                        card_parsed['Card Middle Text'].append([
                            dis.lower() + 's',
                            dis2.lower() + 's',
                            t.group(4)
                        ])
                else:
                    if dis == dis.lower():
                        card_parsed['Card Middle Text'].append(
                            [dis, t.group(4)])
                    else:
                        card_parsed['Card Middle Text'].append(
                            [dis.lower() + 's', t.group(4)])

            # Some workaround to bold 'Strike' and 'Ranged strike'
            elif re.match(r'(Strike\:)', i):
                t = re.match(r'(Strike\:)?\s?(.*)', i)
                card_parsed['Card Middle Text'].append(
                    [t.group(1), t.group(2)])
            elif re.match(r'(Ranged strike\:)', i):
                t = re.match(r'(Ranged strike\:)?\s?(.*)', i)
                card_parsed['Card Middle Text'].append(
                    [t.group(1), t.group(2)])
            else:
                # That is where main text goes
                t = re.match(r'(.*)', i)
                card_parsed['Card Other Text'].append(t.group(1))

        card_parsed['Pool Cost'] = card['Pool Cost']
        card_parsed['Blood Cost'] = card['Blood Cost']
        # Card names can be of any unicode letters, but ascii required for
        # image file name in static/img/*. 'URL Name' used only as file name.
        card_parsed['URL Name'] = letters_to_ascii(
            re.sub('[\\W]', '', card['Name']).lower())
        # 'URL Type' used for iconization of card types in html template
        card_parsed['URL Type'] = []
        type_list = card['Type'].split('/')

        for cardtype in type_list:
            card_parsed['URL Type'].append(
                re.sub('[\\W]', '', cardtype).lower())

        # Id used to unfold card text in result output
        card_parsed['Id'] = card['Id']
        parsed_library.append(card_parsed)

    return parsed_library


def print_library_total(cards):
    total = []
    type_counter = {
        'Master': 0,
        'Action': 0,
        'Action Modifier': 0,
        'Ally': 0,
        'Combat': 0,
        'Equipment': 0,
        'Event': 0,
        'Political Action': 0,
        'Reaction': 0,
        'Retainer': 0,
        # 'Reflex': 0,
        'Conviction': 0,
        'Power': 0,
    }

    for card in cards:
        types = card['Type'].split('/')
        for cardtype in types:
            type_counter[cardtype] += 1

    # total[0] to be total quantity of all matching cards
    total.append(len(cards))

    # total[x] to be list of (type, quantity) matching card types
    # This will later be used in html templatea.
    for cardtype, quantity in type_counter.items():
        if quantity:
            total.append([re.sub('[\\W]', '', cardtype).lower(), quantity])

    return total
