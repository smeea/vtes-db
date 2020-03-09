#!/usr/bin/env python

import json
import re
from app.parse import letters_to_ascii

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
    match_list = card_lists.pop()
    while card_lists:
        pre_match_list = []
        for i in card_lists.pop():
            if i in match_list:
                pre_match_list.append(i)
        match_list = pre_match_list

    return match_list


def parse_library_card(cards):
    parsed_library = []
    for card in cards:
        card_parsed = {}
        card_parsed['Name'] = card['Name']
        card_parsed['Type'] = card['Type']

        if card['Discipline']:
            card_parsed['Discipline'] = re.split('/| & ', card['Discipline'])
            card_parsed['URL Discipline'] = []

            for discipline in card_parsed['Discipline']:
                if discipline == 'Thanatosis':
                    card_parsed['URL Discipline'].append('thn')
                elif discipline == 'Vision':
                    card_parsed['URL Discipline'].append('visi')
                else:
                    card_parsed['URL Discipline'].append(
                        str(discipline[:3].lower()))

            if '/' in card['Discipline']:
                if len(card['Discipline'].split('/')) == 3:
                    card_parsed['URL Discipline'].insert(2, '/')
                card_parsed['URL Discipline'].insert(1, '/')

            if '&' in card['Discipline']:
                card_parsed['URL Discipline'].insert(1, '+')

        if card['Type'] == 'Ally' or card['Type'] == "Retainer":
            life = re.match(r'.*with ([0-9]) life', card['Card Text'])
            card_parsed['Life'] = life.group(1)

        if card['Type'] == 'Ally':
            strength = re.match(r'.*([0-9]) strength', card['Card Text'])
            card_parsed['Strength'] = strength.group(1)

        if card['Clan']:
            card_parsed['URL Clan'] = []
            clan_list = card['Clan'].split('/')
            for clan in clan_list:
                card_parsed['URL Clan'].append(
                    re.sub('[\\W]', '', clan.lower()))
            if '/' in card['Clan']:
                card_parsed['URL Clan'].insert(1, '/')

        card_parsed['Card Text'] = card['Card Text'].split('\n')

        card_title_keywords = [
            'unique', 'weapon', 'vehicle', 'equipment', 'only usable by',
            'requires a', 'gehenna', 'out-of-turn', 'master.', 'master:',
            'trifle.', 'archetype.', 'location.', 'discipline.', 'action.',
            'only usable by', 'only usable before', 'only usable at',
            'only usable if', 'do not replace', 'ammo.', 'aim.'
        ]
        for keyword in card_title_keywords:
            if re.match(r'(?!^\[).*{}'.format(keyword),
                        card_parsed['Card Text'][0].lower()):
                card_parsed['Card Title'] = card_parsed['Card Text'].pop(0)
                break
        card_parsed['Pool Cost'] = card['Pool Cost']
        card_parsed['Blood Cost'] = card['Blood Cost']
        card_parsed['URL Name'] = letters_to_ascii(
            re.sub('[\\W]', '', card['Name']).lower())
        card_parsed['URL Type'] = []
        type_list = card['Type'].split('/')
        for cardtype in type_list:
            card_parsed['URL Type'].append(
                re.sub('[\\W]', '', cardtype).lower())
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
    total.append(len(cards))
    for cardtype, quantity in type_counter.items():
        if quantity:
            total.append([re.sub('[\\W]', '', cardtype).lower(), quantity])
    return total
