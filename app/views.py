#!/usr/bin/env python3

import re
import unicodedata
from flask import Blueprint, render_template, request, flash
from app.search_crypt import get_crypt_by_cardtext
from app.search_crypt import get_crypt_by_trait
from app.search_crypt import get_crypt_by_discipline
from app.search_crypt import get_crypt_by_title
from app.search_crypt import get_crypt_by_votes
from app.search_crypt import get_crypt_by_capacity
from app.search_crypt import get_crypt_by_group
from app.search_crypt import get_crypt_by_sect
from app.search_crypt import get_overall_crypt
from app.search_crypt import parse_crypt_card
from app.search_crypt import print_crypt_total
from app.forms import CryptForm

search = Blueprint('search', __name__, url_prefix='/')


@search.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


@search.route('/crypt', methods=('GET', 'POST'))
def crypt():

    titles = []
    capacity = []
    group = []
    trait = []
    votes = ''
    parameters = 0
    parsed_cards = []
    match_by_category = []
    total = ''

    cryptform = CryptForm(request.form)
    cryptform.titles.choices = [
        # ('kholo', 'Kholo'),
        # ('imperator', 'Imperator'),
        ('primogen', 'Primogen'),
        ('prince', 'Prince'),
        ('justicar', 'Justicar'),
        ('inner circle', 'Inner Circle'),
        ('bishop', 'Bishop'),
        ('archbishop', 'Archbishop'),
        ('priscus', 'Priscus'),
        ('cardinal', 'Cardinal'),
        ('regent', 'Regent'),
        ('magaji', 'Magaji'),
        ('baron', 'Baron'),
        ('1 vote', '1 vote (Independent)'),
        ('2 votes', '2 votes (Independent)')
    ]
    cryptform.trait.choices = [('[:.] \+1 intercept.', '+1 intercept'),
                               ('[:.] \+1 stealth.', '+1 stealth'),
                               ('[:.] \+1 bleed.', '+1 bleed'),
                               ('[:.] \+2 bleed.', '+2 bleed'),
                               ('[:.] \+1 strength.', '+1 strength'),
                               ('[:.] \+2 strength.', '+2 strength'),
                               ('additional strike', 'Additional Strike'),
                               ('optional press', 'Press'),
                               ('enter combat', 'Enter combat'),
                               ('Black Hand[ .:]', 'Black Hand'),
                               ('Seraph[.:]', 'Seraph'),
                               ('Infernal[.:]', 'Infernal'),
                               ('Red List[.:]', 'Red List')]
    cryptform.votes.choices = [('ANY', 'ANY'), ('0', '0'), ('1', '1+'),
                               ('2', '2+'), ('3', '3+'), ('4', '4+')]
    cryptform.sect.choices = [('ANY', 'ANY'), ('Camarilla', 'Camarilla'),
                              ('Sabbat', 'Sabbat'), ('Laibon', 'Laibon'),
                              ('Independent', 'Independent'),
                              ('Anarch', 'Anarch')]
    cryptform.capacitymoreless.choices = [('<=', '<='), ('>=', '>=')]
    cryptform.capacity.choices = [('ANY', 'ANY')]
    for i in range(1, 12):
        cryptform.capacity.choices.append((i, i))
    cryptform.group.choices = []
    for i in range(1, 7):
        cryptform.group.choices.append((i, i))

    if cryptform.is_submitted():
        # Get cards by text
        cardtext = cryptform.cardtext.data
        if cardtext:
            parameters += 1
            cards_by_cardtext = get_crypt_by_cardtext(cardtext)
            match_by_category.append(cards_by_cardtext)

        # Get cards by text trait
        trait = cryptform.trait.data
        if trait:
            parameters += 1
            cards_by_trait = get_crypt_by_trait(trait)
            match_by_category.append(cards_by_trait)

        # Get cards by disciplines
        # TODO Add discipline choices as clickable icons
        disciplines_input = cryptform.disciplines.data
        disciplines = disciplines_input.split()
        if disciplines:
            parameters += 1
            cards_by_disciplines = get_crypt_by_discipline(disciplines)
            match_by_category.append(cards_by_disciplines)

        # Get cards by title
        titles = cryptform.titles.data
        if titles:
            parameters += 1
            cards_by_titles = get_crypt_by_title(titles)
            match_by_category.append(cards_by_titles)

        # Get cards by votes
        votes = cryptform.votes.data
        if votes != 'ANY':
            parameters += 1
            cards_by_votes = get_crypt_by_votes(int(votes))
            match_by_category.append(cards_by_votes)

        # Get cards by capacity
        if cryptform.capacity.data != 'ANY':
            parameters += 1
            if cryptform.capacitymoreless.data == '<=':
                capacity = range(1, int(cryptform.capacity.data) + 1)
            if cryptform.capacitymoreless.data == '>=':
                capacity = range(int(cryptform.capacity.data), 12)
            cards_by_capacity = get_crypt_by_capacity(capacity)
            match_by_category.append(cards_by_capacity)

        # Get cards by group
        group = cryptform.group.data
        if group:
            parameters += 1
            cards_by_group = get_crypt_by_group(group)
            match_by_category.append(cards_by_group)

        # Get cards by sect
        sect = cryptform.sect.data
        if sect != 'ANY':
            parameters += 1
            cards_by_sect = get_crypt_by_sect(sect)
            match_by_category.append(cards_by_sect)

        # Get overall matches & total
        if parameters == 0:
            flash('CHOOSE AT LEAST ONE PARAMETER.')
        else:
            cards = get_overall_crypt(match_by_category)
            if cards:
                total = print_crypt_total(cards)

                # Sort card by capacity, then name
                sorted_cards = (sorted(sorted(cards, key=lambda x: x['Name']),
                                       key=lambda x: x['Capacity']))

                # Parse card text for output
                parsed_cards = parse_crypt_card(sorted_cards)

                def letters_to_ascii(text):
                    return ''.join(c
                                   for c in unicodedata.normalize('NFD', text)
                                   if unicodedata.category(c) != 'Mn')

                for card in parsed_cards:
                    card['ASCII Name'] = letters_to_ascii(
                        re.sub('[\\W]', '', card['Name'].lower()))
                    card['ASCII Clan'] = re.sub('[\\W]', '',
                                                card['Clan']).lower()

            else:
                flash('NO CARDS FOUND. WHY SO GREEDY? :(')

    return render_template(
        'crypt.html',
        form=cryptform,
        cards=parsed_cards,
        # debug=debug,
        total=total)


@search.route('/library', methods=('GET', 'POST'))
def library():
    cards = []
    total = ''
    if request.method == 'POST':
        # input = request.form['input']
        # cards = search_library(input)
        # total = search_library(cards)
        cards = []

    return render_template('library.html', cards=cards, total=total)
