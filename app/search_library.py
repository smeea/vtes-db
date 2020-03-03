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
                card_parsed['URL Discipline'].append(
                    str(discipline[:3].lower()))

            if '/' in card['Discipline']:
                if len(card['Discipline'].split('/')) == 3:
                    card_parsed['URL Discipline'].insert(2, '/')
                card_parsed['URL Discipline'].insert(1, '/')

            if '&' in card['Discipline']:
                card_parsed['URL Discipline'].insert(1, '+')

        card_parsed['Clan'] = card['Clan']
        card_parsed['Card Text'] = card['Card Text']
        card_parsed['Pool Cost'] = card['Pool Cost']
        card_parsed['Blood Cost'] = card['Blood Cost']
        card_parsed['URL Name'] = letters_to_ascii(
            re.sub('[\\W]', '', card['Name']).lower())

        card_parsed['URL Clan'] = re.sub('[\\W]', '', card['Clan']).lower()
        card_parsed['URL Type'] = []
        type_list = card['Type'].split('/')
        for cardtype in type_list:
            card_parsed['URL Type'].append(
                re.sub('[\\W]', '', cardtype).lower())
        parsed_library.append(card_parsed)

    return parsed_library


def print_library_total(cards):
    # Add type counter
    return len(cards)
