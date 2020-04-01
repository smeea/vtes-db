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


# Render index.html page to when user visit main page
@search.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


# Render crypt.html page to when user visit /crypt
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

    # First entry is discipline name for search function
    # Second entry is image name for rendering form icon
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

    # First entry is virtue name for search function
    # Second entry is image name for rendering form icon
    cryptform.virtues.choices = [
        ('ven', 'ven'),
        ('def', 'def'),
        ('inn', 'inn'),
        ('jud', 'jud'),
        ('mar', 'mar'),
        ('red', 'red'),
        ('visi', 'visi'),
    ]

    # First entry is title name for search function
    # Second entry is search form entry (can be changed without breaking things)
    cryptform.titles.choices = [
        ('primogen', 'Primogen'),
        ('prince', 'Prince'),
        ('justicar', 'Justicar'),
        # ('imperator', 'Imperator'),
        ('inner circle', 'Inner Circle'),
        ('baron', 'Baron'),
        ('1 vote', '1 vote (Independent)'),
        ('2 votes', '2 votes (Independent)'),
        ('bishop', 'Bishop'),
        ('archbishop', 'Archbishop'),
        ('priscus', 'Priscus'),
        ('cardinal', 'Cardinal'),
        ('regent', 'Regent'),
        ('magaji', 'Magaji'),
        # ('3 votes', '3 votes (Independent)'),
    ]

    # First entry is trait regexp for search function
    # Second entry is trait form entry (can be changed without breaking things)
    # 'Trait' is just part of the card text which is widely available among cards
    #
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

    # First entry is votes value for search function
    # Second entry is votes form entry (can be changed without breaking things)
    cryptform.votes.choices = [('ANY', 'ANY'), ('0', '0'), ('1', '1+'),
                               ('2', '2+'), ('3', '3+'), ('4', '4+')]

    # First entry is sect value for search function
    # Second entry is sect form entry (can be changed without breaking things)
    cryptform.sect.choices = [
        ('ANY', 'ANY'),
        ('Camarilla', 'Camarilla'),
        ('Sabbat', 'Sabbat'),
        ('Laibon', 'Laibon'),
        ('Independent', 'Independent'),
        ('Anarch', 'Anarch'),
        ('Imbued', 'Imbued'),
    ]

    # First entry is clan value for search function
    # Second entry is clan form entry (can be changed without breaking things)
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
        ('Daughter of Cacophony', 'Daughter of Cacophony'),
        ('Follower of Set', 'Follower of Set'),
        ('Gangrel', 'Gangrel'),
        ('Gangrel antitribu', 'Gangrel Antitribu'),
        ('Gargoyle', 'Gargoyle'),
        ('Giovanni', 'Giovanni'),
        ('Guruhi', 'Guruhi'),
        ('Harbinger of Skulls', 'Harbinger of Skulls'),
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
    # Generating capacity form entries 1...11, same as above
    for i in range(1, 12):
        cryptform.capacity.choices.append((i, i))

    cryptform.group.choices = []
    # Generating group form entries 1...6, same as above
    for i in range(1, 7):
        cryptform.group.choices.append((i, i))

    if cryptform.is_submitted():
        # The code below executed after SEARCH button submitted in /crypt

        # Get cards by text
        cardtext = cryptform.cardtext.data
        if cardtext:
            # 'parameters' value (here and below) used later to decide if card
            # is matching all of given parameters. It is incremented each time
            # new filter (form) have any value (i.e. user changed it).
            parameters += 1
            cards_by_cardtext = get_crypt_by_cardtext(cardtext)
            # 'match_by_category' is list of all cards matching by any
            # of the active filters
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
        # 'ANY' used as 'default' value of the form (first in the form-choices
        # lists above). With value 'ANY' filter will not run.
        if votes != 'ANY':
            parameters += 1
            cards_by_votes = get_crypt_by_votes(int(votes))
            match_by_category.append(cards_by_votes)

        # Get cards by capacity
        if cryptform.capacity.data != 'ANY':
            parameters += 1
            capacity = int(cryptform.capacity.data)
            moreless = cryptform.capacitymoreless.data
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
            # Message to user when SEARCH button submitted with all forms
            # empty (or default i.e. 'ANY')
            flash('CHOOSE AT LEAST ONE PARAMETER.')
        else:
            # Getting only cards matching all filters
            # (from cards matching any filter in 'match_by_category' list)
            cards = get_overall_crypt(match_by_category)
            if cards:
                total = print_crypt_total(cards)

                # Sort result cards in the following order:
                # Capacity -> Group -> Clan -> Name
                sorted_cards = (sorted(sorted(sorted(sorted(
                    cards, key=lambda x: x['Name']),
                                                     key=lambda x: x['Clan']),
                                              key=lambda x: x['Group']),
                                       key=lambda x: x['Capacity']))

                # Parse result cards for output to 'html'.
                # parsed_crypt_cards list is then sent to templates/crypt.html,
                # where it will be parsed using Jinja2).
                parsed_crypt_cards = parse_crypt_card(sorted_cards)

            else:
                # Message to user when SEARCH button submitted but
                # no cards found to match the filters
                flash('NO CARDS FOUND.')

    # Return template/crypt.html page (with results, if any - but also used
    # for direct visits to vtes-db/crypt.html)
    return render_template(
        'crypt.html',
        # Search forms
        form=cryptform,
        # Search results (matching cards)
        cards=parsed_crypt_cards,
        # String with summary of total cards found
        total=total)


# SEE ABOVE - GENERALLY SAME AS FOR /crypt, BUT FOR /library
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
        ('Daughter of Cacophony', 'Daughter of Cacophony'),
        ('Follower of Set', 'Follower of Set'),
        ('Gangrel', 'Gangrel'),
        ('Gangrel antitribu', 'Gangrel Antitribu'),
        ('Gargoyle', 'Gargoyle'),
        ('Giovanni', 'Giovanni'),
        ('Guruhi', 'Guruhi'),
        ('Harbinger of Skulls', 'Harbinger of Skulls'),
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
         '+Intercept / -Stealth'),
        ('\+[0-9]+ stealth(?! \(d\))(?! \w)(?! action)|\-[0-9]+ intercept',
         '+Stealth / -Intercept'),
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
