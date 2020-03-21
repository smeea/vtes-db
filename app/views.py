from flask import Blueprint, render_template, request, flash
from app.search_crypt import get_crypt_by_cardtext
from app.search_crypt import get_crypt_by_trait
from app.search_crypt import get_crypt_by_discipline
from app.search_crypt import get_crypt_by_virtues
from app.search_crypt import get_crypt_by_title
from app.search_crypt import get_crypt_by_votes
from app.search_crypt import get_crypt_by_capacity
from app.search_crypt import get_crypt_by_group
from app.search_crypt import get_crypt_by_sect
from app.search_crypt import get_crypt_by_clan
from app.search_crypt import get_overall_crypt
from app.search_crypt import parse_crypt_card
from app.search_crypt import print_crypt_total
from app.search_library import get_library_by_cardtext
from app.search_library import get_library_by_trait
from app.search_library import get_library_by_discipline
from app.search_library import get_library_by_title
from app.search_library import get_library_by_sect
from app.search_library import get_library_by_clan
from app.search_library import get_library_by_cardtype
from app.search_library import get_library_by_blood
from app.search_library import get_library_by_pool
from app.search_library import get_overall_library
from app.search_library import parse_library_card
from app.search_library import print_library_total
from app.forms import CryptForm
from app.forms import LibraryForm

search = Blueprint('search', __name__, url_prefix='/')


@search.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


@search.route('/crypt', methods=('GET', 'POST'))
def crypt():

    titles = []
    disciplines = []
    virtues = []
    capacity = []
    group = []
    trait = []
    match_by_category = []
    parsed_crypt_cards = []
    parameters = 0
    total = ''

    cryptform = CryptForm(request.form)

    cryptform.disciplines.choices = [
        ('abo', 'abo'),
        ('ABO', 'abos'),
        ('ani', 'ani'),
        ('ANI', 'anis'),
        ('aus', 'aus'),
        ('AUS', 'auss'),
        ('cel', 'cel'),
        ('CEL', 'cels'),
        ('chi', 'chi'),
        ('CHI', 'chis'),
        ('dai', 'dai'),
        ('DAI', 'dais'),
        ('dom', 'dom'),
        ('DOM', 'doms'),
        ('dem', 'dem'),
        ('DEM', 'dems'),
        ('for', 'for'),
        ('FOR', 'fors'),
        # ('mal', 'mal'), ('MAL', 'mals'),
        ('mel', 'mel'),
        ('MEL', 'mels'),
        ('myt', 'myt'),
        ('MYT', 'myts'),
        ('nec', 'nec'),
        ('NEC', 'necs'),
        ('obe', 'obe'),
        ('OBE', 'obes'),
        ('obf', 'obf'),
        ('OBF', 'obfs'),
        ('obt', 'obt'),
        ('OBT', 'obts'),
        ('pot', 'pot'),
        ('POT', 'pots'),
        ('pre', 'pre'),
        ('PRE', 'pres'),
        ('pro', 'pro'),
        ('PRO', 'pros'),
        ('san', 'san'),
        ('SAN', 'sans'),
        ('ser', 'ser'),
        ('SER', 'sers'),
        ('spi', 'spi'),
        ('SPI', 'spis'),
        # ('str', 'str'), ('STR', 'strs'),
        ('tem', 'tem'),
        ('TEM', 'tems'),
        ('thn', 'thn'),
        ('THN', 'thns'),
        ('tha', 'tha'),
        ('THA', 'thas'),
        ('qui', 'qui'),
        ('QUI', 'quis'),
        ('val', 'val'),
        ('VAL', 'vals'),
        ('vic', 'vic'),
        ('VIC', 'vics'),
        ('vis', 'vis'),
        ('VIS', 'viss')
    ]

    cryptform.virtues.choices = [
        ('ven', 'ven'),
        ('def', 'def'),
        ('inn', 'inn'),
        ('jud', 'jud'),
        ('mar', 'mar'),
        ('red', 'red'),
        ('visi', 'visi'),
    ]

    cryptform.titles.choices = [
        ('primogen', 'Primogen'),
        ('prince', 'Prince'),
        ('justicar', 'Justicar'),
        # ('imperator', 'Imperator'),
        ('inner circle', 'Inner Circle'),
        ('magaji', 'Magaji'),
        ('bishop', 'Bishop'),
        ('archbishop', 'Archbishop'),
        ('priscus', 'Priscus'),
        ('cardinal', 'Cardinal'),
        ('regent', 'Regent'),
        ('baron', 'Baron'),
        ('1 vote', '1 vote (Independent)'),
        ('2 votes', '2 votes (Independent)'),
        # ('3 votes', '3 votes (Independent)'),
    ]

    cryptform.trait.choices = [('[:.] \+1 intercept.', '+1 intercept'),
                               ('[:.] \+1 stealth.', '+1 stealth'),
                               ('[:.] \+1 bleed.', '+1 bleed'),
                               ('[:.] \+2 bleed.', '+2 bleed'),
                               ('[:.] \+1 strength.', '+1 strength'),
                               ('[:.] \+2 strength.', '+2 strength'),
                               ('additional strike', 'Additional Strike'),
                               ('optional maneuver', 'Maneuver'),
                               ('optional press', 'Press'),
                               ('(?<!non-)aggravated', 'Aggravated'),
                               ('enter combat', 'Enter combat'),
                               ('black hand[ .:]', 'Black Hand'),
                               ('seraph[.:]', 'Seraph'),
                               ('infernal[.:]', 'Infernal'),
                               ('red list[.:]', 'Red List'),
                               ('\[flight\]\.', 'Flight')]

    cryptform.votes.choices = [('ANY', 'ANY'), ('0', '0'), ('1', '1+'),
                               ('2', '2+'), ('3', '3+'), ('4', '4+')]

    cryptform.sect.choices = [
        ('ANY', 'ANY'),
        ('Camarilla', 'Camarilla'),
        ('Sabbat', 'Sabbat'),
        ('Laibon', 'Laibon'),
        ('Independent', 'Independent'),
        ('Anarch', 'Anarch'),
        ('Imbued', 'Imbued'),
    ]

    cryptform.clan.choices = [
        ('ANY', 'ANY'),
        ('Abomination', 'Abomination'),
        ('Ahrimane', 'Ahrimane'),
        ('Akunanse', 'Akunanse'),
        ('Assamite', 'Assamite'),
        ('Baali', 'Baali'),
        ('Blood Brother', 'Blood Brother'),
        ('Brujah', 'Brujah'),
        ('Brujah antitribu', 'Brujah Antitribu'),
        ('Caitiff', 'Caitiff'),
        ('Daughter of Cacophony', 'Daughter Of Cacophony'),
        ('Follower Of Set', 'Follower Of Set'),
        ('Gangrel', 'Gangrel'),
        ('Gangrel antitribu', 'Gangrel Antitribu'),
        ('Gargoyle', 'Gargoyle'),
        ('Giovanni', 'Giovanni'),
        ('Guruhi', 'Guruhi'),
        ('Harbinger Of Skulls', 'Harbinger Of Skulls'),
        ('Ishtarri', 'Ishtarri'),
        ('Kiasyd', 'Kiasyd'),
        ('Lasombra', 'Lasombra'),
        ('Malkavian', 'Malkavian'),
        ('Malkavian antitribu', 'Malkavian Antitribu'),
        ('Nagaraja', 'Nagaraja'),
        ('Nosferatu', 'Nosferatu'),
        ('Nosferatu antitribu', 'Nosferatu Antitribu'),
        ('Osebo', 'Osebo'),
        ('Pander', 'Pander'),
        ('Ravnos', 'Ravnos'),
        ('Salubri', 'Salubri'),
        ('Salubri antitribu', 'Salubri Antitribu'),
        ('Samedi', 'Samedi'),
        ('Toreador', 'Toreador'),
        ('Toreador antitribu', 'Toreador Antitribu'),
        ('Tremere', 'Tremere'),
        ('Tremere antitribu', 'Tremere Antitribu'),
        ('True Brujah', 'True Brujah'),
        ('Tzimisce', 'Tzimisce'),
        ('Ventrue', 'Ventrue'),
        ('Ventrue antitribu', 'Ventrue Antitribu'),
        ('', ''),
        ('Avenger', 'Avenger'),
        ('Defender', 'Defender'),
        ('Innocent', 'Innocent'),
        ('Judge', 'Judge'),
        ('Martyr', 'Martyr'),
        ('Redeemer', 'Redeemer'),
        ('Visionary', 'Visionary'),
    ]

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
        disciplines = cryptform.disciplines.data
        if disciplines:
            parameters += 1
            cards_by_disciplines = get_crypt_by_discipline(disciplines)
            match_by_category.append(cards_by_disciplines)

        # Get cards by virtues
        virtues = cryptform.virtues.data
        if virtues:
            parameters += 1
            cards_by_virtues = get_crypt_by_virtues(virtues)
            match_by_category.append(cards_by_virtues)

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
            capacity = int(cryptform.capacity.data)
            moreless = cryptform.capacitymoreless.data
            #     capacity = range(1, int(cryptform.capacity.data) + 1)
            # if cryptform.capacitymoreless.data == '>=':
            #     capacity = range(int(cryptform.capacity.data), 12)
            cards_by_capacity = get_crypt_by_capacity(capacity, moreless)
            match_by_category.append(cards_by_capacity)

        # Get cards by group
        group = cryptform.group.data
        if group:
            parameters += 1
            cards_by_group = get_crypt_by_group(group)
            match_by_category.append(cards_by_group)

        # Get cards by clan
        clan = cryptform.clan.data
        if clan != 'ANY':
            parameters += 1
            cards_by_clan = get_crypt_by_clan(clan)
            match_by_category.append(cards_by_clan)

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

                # Sort card by capacity, name
                sorted_cards = (sorted(sorted(cards, key=lambda x: x['Name']),
                                       key=lambda x: x['Capacity']))

                # Parse card text for output
                parsed_crypt_cards = parse_crypt_card(sorted_cards)

            else:
                flash('NO CARDS FOUND.')

    return render_template('crypt.html',
                           form=cryptform,
                           cards=parsed_crypt_cards,
                           total=total)


@search.route('/library', methods=('GET', 'POST'))
def library():

    parameters = 0
    parsed_library_cards = []
    match_by_category = []
    total = ''

    libraryform = LibraryForm(request.form)
    libraryform.title.choices = [
        ('ANY', 'ANY'),
        ('primogen', 'Primogen'),
        ('prince', 'Prince'),
        ('justicar', 'Justicar'),
        # ('imperator', 'Imperator'),
        ('inner circle', 'Inner Circle'),
        ('magaji', 'Magaji'),
        ('bishop', 'Bishop'),
        ('archbishop', 'Archbishop'),
        ('priscus', 'Priscus'),
        ('cardinal', 'Cardinal'),
        ('regent', 'Regent'),
        ('baron', 'Baron'),
        ('1 vote', '1 vote (Independent)'),
        ('2 votes', '2 votes (Independent)'),
        # ('3 votes', '3 votes (Independent)'),
    ]

    libraryform.discipline.choices = [
        ('ANY', 'ANY'),
        ('Auspex', 'Auspex'),
        ('Abombwe', 'Abombwe'),
        ('Animalism', 'Animalism'),
        ('Celerity', 'Celerity'),
        ('Chimerstry', 'Chimerstry'),
        ('Daimoinon', 'Daimoinon'),
        ('Dementation', 'Dementation'),
        ('Dominate', 'Dominate'),
        ('Flight', 'Flight'),
        ('Fortitude', 'Fortitude'),
        # ('Maleficia', 'Maleficia'),
        ('Melpominee', 'Melpominee'),
        ('Mytherceria', 'Mytherceria'),
        ('Necromancy', 'Necromancy'),
        ('Obeah', 'Obeah'),
        ('Obfuscate', 'Obfuscate'),
        ('Obtenebration', 'Obtenebration'),
        ('Potence', 'Potence'),
        ('Presence', 'Presence'),
        ('Protean', 'Protean'),
        ('Serpentis', 'Serpentis'),
        ('Sanguinus', 'Sanguinus'),
        ('Spiritus', 'Spiritus'),
        # ('Striga', 'Striga'),
        ('Temporis', 'Temporis'),
        ('Thanatosis', 'Thanatosis'),
        ('Thaumaturgy', 'Thaumaturgy'),
        ('Quietus', 'Quietus'),
        ('Valeren', 'Valeren'),
        ('Vicissitude', 'Vicissitude'),
        ('Visceratika', 'Visceratika'),
        ('', ''),
        ('Defense', 'Defense'),
        ('Innocence', 'Innocence'),
        ('Judgment', 'Judgment'),
        ('Martyrdom', 'Martyrdom'),
        ('Redemption', 'Redemption'),
        ('Vengeance', 'Vengeance'),
        ('Vision', 'Vision'),
    ]

    libraryform.cardtype.choices = [
        ('ANY', 'ANY'),
        ('Master', 'Master'),
        ('Action', 'Action'),
        ('Action Modifier', 'Action Modifier'),
        ('Ally', 'Ally'),
        ('Combat', 'Combat'),
        ('Equipment', 'Equipment'),
        ('Event', 'Event'),
        ('Political Action', 'Political Action'),
        ('Reaction', 'Reaction'),
        ('Retainer', 'Retainer'),
        # ('Reflex', 'Reflex'),
        ('', ''),
        ('Conviction', 'Conviction'),
        ('Power', 'Power'),
    ]

    libraryform.sect.choices = [('ANY', 'ANY'), ('camarilla', 'Camarilla'),
                                ('sabbat', 'Sabbat'), ('laibon', 'Laibon'),
                                ('independent', 'Independent'),
                                ('anarch', 'Anarch'), ('imbued', 'Imbued')]

    libraryform.clan.choices = [
        ('ANY', 'ANY'),
        ('Abomination', 'Abomination'),
        ('Ahrimane', 'Ahrimane'),
        ('Akunanse', 'Akunanse'),
        ('Assamite', 'Assamite'),
        ('Baali', 'Baali'),
        ('Blood Brother', 'Blood Brother'),
        ('Brujah', 'Brujah'),
        ('Brujah antitribu', 'Brujah Antitribu'),
        ('Caitiff', 'Caitiff'),
        ('Daughter of Cacophony', 'Daughter Of Cacophony'),
        ('Follower Of Set', 'Follower Of Set'),
        ('Gangrel', 'Gangrel'),
        ('Gangrel antitribu', 'Gangrel Antitribu'),
        ('Gargoyle', 'Gargoyle'),
        ('Giovanni', 'Giovanni'),
        ('Guruhi', 'Guruhi'),
        ('Harbinger Of Skulls', 'Harbinger Of Skulls'),
        ('Ishtarri', 'Ishtarri'),
        ('Kiasyd', 'Kiasyd'),
        ('Lasombra', 'Lasombra'),
        ('Malkavian', 'Malkavian'),
        ('Malkavian antitribu', 'Malkavian Antitribu'),
        ('Nagaraja', 'Nagaraja'),
        ('Nosferatu', 'Nosferatu'),
        ('Nosferatu antitribu', 'Nosferatu Antitribu'),
        ('Osebo', 'Osebo'),
        ('Pander', 'Pander'),
        ('Ravnos', 'Ravnos'),
        ('Salubri', 'Salubri'),
        ('Salubri antitribu', 'Salubri Antitribu'),
        ('Samedi', 'Samedi'),
        ('Toreador', 'Toreador'),
        ('Toreador antitribu', 'Toreador Antitribu'),
        ('Tremere', 'Tremere'),
        ('Tremere antitribu', 'Tremere Antitribu'),
        ('True Brujah', 'True Brujah'),
        ('Tzimisce', 'Tzimisce'),
        ('Ventrue', 'Ventrue'),
        ('Ventrue antitribu', 'Ventrue Antitribu'),
        ('', ''),
        ('Avenger', 'Avenger'),
        ('Defender', 'Defender'),
        ('Innocent', 'Innocent'),
        ('Judge', 'Judge'),
        ('Martyr', 'Martyr'),
        ('Redeemer', 'Redeemer'),
        ('Visionary', 'Visionary'),
    ]

    libraryform.bloodmoreless.choices = [('<=', '<='), ('>=', '>=')]
    libraryform.blood.choices = [('ANY', 'ANY')]
    for i in range(0, 5):
        libraryform.blood.choices.append((i, i))

    libraryform.poolmoreless.choices = [('<=', '<='), ('>=', '>=')]
    libraryform.pool.choices = [('ANY', 'ANY')]
    for i in range(0, 7):
        libraryform.pool.choices.append((i, i))

    libraryform.trait.choices = [
        ('\-[0-9]+ stealth(?! \(d\))(?! \w)(?! action)|\+[0-9]+ intercept',
         '+Intercept / -St'),
        ('\+[0-9]+ stealth(?! \(d\))(?! \w)(?! action)|\-[0-9]+ intercept',
         '+Stealth / -Int'),
        ('\+[0-9]+ bleed', '+Bleed'),
        ('\+[0-9]+ strength', '+Strength'),
        ('dodge', 'Dodge'),
        ('maneuver', 'Maneuver'),
        ('additional strike', 'Additional Strike'),
        ('(?<!non-)aggravated', 'Aggravated'),
        ('(?<!un)prevent', 'Prevent'),
        ('(optional )?press', 'Press'),
        ('combat ends', 'Combat Ends'),
        ('enter combat', 'Enter Combat'),
        ('change the target of the bleed|is now bleeding', 'Bounce Bleed'),
        ('black hand', 'Black Hand'),
        ('seraph', 'Seraph'),
        ('anarch', 'Anarch'),
        ('infernal', 'Infernal'),
    ]

    if libraryform.is_submitted():
        # Get cards by text
        cardtext = libraryform.cardtext.data
        if cardtext:
            parameters += 1
            cards_by_cardtext = get_library_by_cardtext(cardtext)
            match_by_category.append(cards_by_cardtext)

        # Get cards by trait
        trait = libraryform.trait.data
        if trait:
            parameters += 1
            cards_by_trait = get_library_by_trait(trait)
            match_by_category.append(cards_by_trait)

        # Get cards by type
        cardtype = libraryform.cardtype.data
        if cardtype != 'ANY':
            parameters += 1
            cards_by_cardtype = get_library_by_cardtype(cardtype)
            match_by_category.append(cards_by_cardtype)

        # Get cards by disciplines
        discipline = libraryform.discipline.data
        if discipline != 'ANY':
            parameters += 1
            cards_by_discipline = get_library_by_discipline(discipline)
            match_by_category.append(cards_by_discipline)

        # Get cards by title
        title = libraryform.title.data
        if title != 'ANY':
            parameters += 1
            cards_by_title = get_library_by_title(title)
            match_by_category.append(cards_by_title)

        # Get cards by sect
        sect = libraryform.sect.data
        if sect != 'ANY':
            parameters += 1
            cards_by_sect = get_library_by_sect(sect)
            match_by_category.append(cards_by_sect)

        # Get cards by clan
        clan = libraryform.clan.data
        if clan != 'ANY':
            parameters += 1
            cards_by_clan = get_library_by_clan(clan)
            match_by_category.append(cards_by_clan)

        # Get cards by blood cost
        if libraryform.blood.data != 'ANY':
            parameters += 1
            blood = libraryform.blood.data
            moreless = libraryform.bloodmoreless.data
            cards_by_blood = get_library_by_blood(blood, moreless)
            match_by_category.append(cards_by_blood)

        # Get cards by pool cost
        if libraryform.pool.data != 'ANY':
            parameters += 1
            pool = libraryform.pool.data
            moreless = libraryform.poolmoreless.data
            cards_by_pool = get_library_by_pool(pool, moreless)
            match_by_category.append(cards_by_pool)

        # Get overall matches & total
        if parameters == 0:
            flash('CHOOSE AT LEAST ONE PARAMETER.')
        else:
            cards = get_overall_library(match_by_category)
            if cards:
                total = print_library_total(cards)

                # Sort card by discipline, clan, name
                sorted_cards = sorted(sorted(sorted(sorted(
                    cards, key=lambda x: x['Name']),
                                                    key=lambda x: x['Type']),
                                             key=lambda x: x['Clan']),
                                      key=lambda x: x['Discipline'])

                # Parse card text for output
                parsed_library_cards = parse_library_card(sorted_cards)

            else:
                flash('NO CARDS FOUND.')

    return render_template('library.html',
                           form=libraryform,
                           cards=parsed_library_cards,
                           total=total)
