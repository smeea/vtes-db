import os
from flask import render_template, flash, send_from_directory
# from flask import redirect, url_for, request
# from flask_login import current_user, login_user, logout_user, login_required
# from werkzeug.urls import url_parse

from app import app
# from app import db
# from app.models import User
# from app.forms import LoginForm
# from app.forms import RegistrationForm
from app.forms import CryptSearchForm
from app.forms import LibrarySearchForm
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
from app.search_crypt import sort_crypt_cards_default
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


# Render favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico',
                               mimetype='image/x-icon')


# Render index.html page to when user visit main page
@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


# Render login.html page to when user visit /login page
# Accounts are not used for anything now.
# login, logout and register are done 'just-in-case'
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         flash('Logged as {}'.format(user.username))
#         return redirect(next_page)
#     return render_template('login.html', form=form)

# Logout when user visit /logout
# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

# Render register.html page to when user visit /register
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)


# Render crypt.html page to when user visit /crypt
@app.route('/crypt', methods=('GET', 'POST'))
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

    cryptsearchform = CryptSearchForm()

    # First entry is discipline name for search function
    # Second entry is image name for rendering form icon
    cryptsearchform.disciplines.choices = [
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
    cryptsearchform.virtues.choices = [
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
    cryptsearchform.titles.choices = [
        ('primogen', 'Primogen: 1'),
        ('prince', 'Prince: 2'),
        ('justicar', 'Justicar: 3'),
        # ('imperator', 'Imperator'),
        ('inner circle', 'Inner Circle: 4'),
        ('baron', 'Baron: 2'),
        ('1 vote', '1 vote (Independent)'),
        ('2 votes', '2 votes (Independent)'),
        ('bishop', 'Bishop: 1'),
        ('archbishop', 'Archbishop: 2'),
        ('priscus', 'Priscus: 3*'),
        ('cardinal', 'Cardinal: 3'),
        ('regent', 'Regent: 4'),
        ('magaji', 'Magaji: 2'),
        # ('3 votes', '3 votes (Independent)'),
    ]

    # First entry is trait regexp for search function
    # Second entry is trait form entry (can be changed without breaking things)
    # 'Trait' is just part of the card text which is widely available among cards
    #
    cryptsearchform.trait.choices = [('[:.] \+1 intercept.', '+1 intercept'),
                                     ('[:.] \+1 stealth.', '+1 stealth'),
                                     ('[:.] \+1 bleed.', '+1 bleed'),
                                     ('[:.] \+2 bleed.', '+2 bleed'),
                                     ('[:.] \+1 strength.', '+1 strength'),
                                     ('[:.] \+2 strength.', '+2 strength'),
                                     ('additional strike',
                                      'Additional Strike'),
                                     ('optional maneuver', 'Maneuver'),
                                     ('optional press', 'Press'),
                                     ('(?<!un)prevent(?<!able)', 'Prevent'),
                                     ('(?<!non-)aggravated', 'Aggravated'),
                                     ('enter combat', 'Enter combat'),
                                     ('black hand[ .:]', 'Black Hand'),
                                     ('seraph[.:]', 'Seraph'),
                                     ('infernal[.:]', 'Infernal'),
                                     ('red list[.:]', 'Red List'),
                                     ('\[flight\]\.', 'Flight')]

    # First entry is votes value for search function
    # Second entry is votes form entry (can be changed without breaking things)
    cryptsearchform.votes.choices = [('ANY', 'ANY'), ('0', '0'), ('1', '1+'),
                                     ('2', '2+'), ('3', '3+'), ('4', '4+')]

    # First entry is sect value for search function
    # Second entry is sect form entry (can be changed without breaking things)
    cryptsearchform.sect.choices = [
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
    cryptsearchform.clan.choices = [
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
        ('Avenger', 'Avenger'),
        ('Defender', 'Defender'),
        ('Innocent', 'Innocent'),
        ('Judge', 'Judge'),
        ('Martyr', 'Martyr'),
        ('Redeemer', 'Redeemer'),
        ('Visionary', 'Visionary'),
    ]

    cryptsearchform.capacitymoreless.choices = [('<=', '<='), ('==', '=='),
                                                ('>=', '>=')]
    cryptsearchform.capacity.choices = [('ANY', 'ANY')]
    # Generating capacity form entries 1...11, same as above
    for i in range(1, 12):
        cryptsearchform.capacity.choices.append((i, i))

    cryptsearchform.group.choices = []
    # Generating group form entries 1...6, same as above
    for i in range(1, 7):
        cryptsearchform.group.choices.append((i, i))

    if cryptsearchform.is_submitted():
        # The code below executed after SEARCH button submitted in /crypt

        # Get cards by text
        cardtext = cryptsearchform.cardtext.data
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
        trait = cryptsearchform.trait.data
        if trait:
            parameters += 1
            cards_by_trait = get_crypt_by_trait(trait)
            match_by_category.append(cards_by_trait)

        # Get cards by disciplines
        disciplines = cryptsearchform.disciplines.data
        if disciplines:
            parameters += 1
            cards_by_disciplines = get_crypt_by_discipline(disciplines)
            match_by_category.append(cards_by_disciplines)

        # Get cards by virtues
        virtues = cryptsearchform.virtues.data
        if virtues:
            parameters += 1
            cards_by_virtues = get_crypt_by_virtues(virtues)
            match_by_category.append(cards_by_virtues)

        # Get cards by title
        titles = cryptsearchform.titles.data
        if titles:
            parameters += 1
            cards_by_titles = get_crypt_by_title(titles)
            match_by_category.append(cards_by_titles)

        # Get cards by votes
        votes = cryptsearchform.votes.data
        # 'ANY' used as 'default' value of the form (first in the form-choices
        # lists above). With value 'ANY' filter will not run.
        if votes != 'ANY':
            parameters += 1
            cards_by_votes = get_crypt_by_votes(int(votes))
            match_by_category.append(cards_by_votes)

        # Get cards by capacity
        if cryptsearchform.capacity.data != 'ANY':
            capacity = int(cryptsearchform.capacity.data)
            parameters += 1
            moreless = cryptsearchform.capacitymoreless.data
            cards_by_capacity = get_crypt_by_capacity(capacity, moreless)
            match_by_category.append(cards_by_capacity)

        # Get cards by group
        group = cryptsearchform.group.data
        if group:
            parameters += 1
            cards_by_group = get_crypt_by_group(group)
            match_by_category.append(cards_by_group)

        # Get cards by clan
        clan = cryptsearchform.clan.data
        if clan != 'ANY':
            parameters += 1
            cards_by_clan = get_crypt_by_clan(clan)
            match_by_category.append(cards_by_clan)

        # Get cards by sect
        sect = cryptsearchform.sect.data
        if sect != 'ANY':
            parameters += 1
            cards_by_sect = get_crypt_by_sect(sect)
            match_by_category.append(cards_by_sect)

        # Get overall matches & total
        if parameters == 0:
            # Message to user when SEARCH button submitted with all forms
            # empty (or default i.e. 'ANY')
            flash('CHOOSE AT LEAST ONE PARAMETER')
        else:
            # Getting only cards matching all filters
            # (from cards matching any filter in 'match_by_category' list)
            cards = get_overall_crypt(match_by_category)
            if cards:
                total = print_crypt_total(cards)

                # Sort result cards in the following order:
                # Capacity -> Group -> Clan -> Name
                sorted_cards = sort_crypt_cards_default(cards)

                # Parse result cards for output to 'html'.
                # parsed_crypt_cards list is then sent to templates/crypt.html,
                # where it will be parsed using Jinja2).
                parsed_crypt_cards = parse_crypt_card(sorted_cards)

            else:
                # Message to user when SEARCH button submitted but
                # no cards found to match the filters
                flash('NO CARDS FOUND')

    # Return template/crypt.html page (with results, if any - but also used
    # for direct visits to vtes-db/crypt.html)
    return render_template(
        'crypt.html',
        # Search forms
        searchform=cryptsearchform,
        # Search results (matching cards)
        cards=parsed_crypt_cards,
        # String with summary of total cards found
        total=total)


# SEE ABOVE - GENERALLY SAME AS FOR /crypt, BUT FOR /library
@app.route('/library', methods=('GET', 'POST'))
def library():

    parameters = 0
    parsed_library_cards = []
    match_by_category = []
    total = ''

    librarysearchform = LibrarySearchForm()

    librarysearchform.title.choices = [
        ('ANY', 'ANY'),
        ('primogen', 'Primogen: 1'),
        ('prince', 'Prince: 2'),
        ('justicar', 'Justicar: 3'),
        # ('imperator', 'Imperator'),
        ('inner circle', 'Inner Circle: 4'),
        ('baron', 'Baron: 2'),
        ('1 vote', '1 vote (Independent)'),
        ('2 votes', '2 votes (Independent)'),
        ('bishop', 'Bishop: 1'),
        ('archbishop', 'Archbishop: 2'),
        ('priscus', 'Priscus: 3*'),
        ('cardinal', 'Cardinal: 3'),
        ('regent', 'Regent: 4'),
        ('magaji', 'Magaji: 2'),
        # ('3 votes', '3 votes (Independent)'),
    ]

    librarysearchform.discipline.choices = [
        ('ANY', 'ANY'),
        ('Auspex', 'Auspex'),
        ('Abombwe', 'Abombwe'),
        ('Animalism', 'Animalism'),
        ('Celerity', 'Celerity'),
        ('Chimerstry', 'Chimerstry'),
        ('Daimoinon', 'Daimoinon'),
        ('Dementation', 'Dementation'),
        ('Dominate', 'Dominate'),
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
        ('Flight', 'Flight'),
        ('Defense', 'Defense'),
        ('Innocence', 'Innocence'),
        ('Judgment', 'Judgment'),
        ('Martyrdom', 'Martyrdom'),
        ('Redemption', 'Redemption'),
        ('Vengeance', 'Vengeance'),
        ('Vision', 'Vision'),
    ]

    librarysearchform.cardtype.choices = [
        ('ANY', 'ANY'),
        ('Action', 'Action'),
        ('Action Modifier', 'Action Modifier'),
        ('Ally', 'Ally'),
        ('Combat', 'Combat'),
        ('Equipment', 'Equipment'),
        ('Event', 'Event'),
        ('Master', 'Master'),
        ('Political Action', 'Political Action'),
        ('Reaction', 'Reaction'),
        ('Retainer', 'Retainer'),
        # ('Reflex', 'Reflex'),
        ('Conviction', 'Conviction'),
        ('Power', 'Power'),
    ]

    librarysearchform.sect.choices = [
        ('ANY', 'ANY'), ('camarilla', 'Camarilla'), ('sabbat', 'Sabbat'),
        ('laibon', 'Laibon'), ('independent', 'Independent'),
        ('anarch', 'Anarch'), ('imbued', 'Imbued')
    ]

    librarysearchform.clan.choices = [
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
        ('Avenger', 'Avenger'),
        ('Defender', 'Defender'),
        ('Innocent', 'Innocent'),
        ('Judge', 'Judge'),
        ('Martyr', 'Martyr'),
        ('Redeemer', 'Redeemer'),
        ('Visionary', 'Visionary'),
    ]

    librarysearchform.bloodmoreless.choices = [('<=', '<='), ('==', '=='),
                                               ('>=', '>=')]
    librarysearchform.blood.choices = [('ANY', 'ANY')]
    for i in range(0, 5):
        librarysearchform.blood.choices.append((i, i))

    librarysearchform.poolmoreless.choices = [('<=', '<='), ('==', '=='),
                                              ('>=', '>=')]
    librarysearchform.pool.choices = [('ANY', 'ANY')]
    for i in range(0, 7):
        librarysearchform.pool.choices.append((i, i))

    librarysearchform.trait.choices = [
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

    if librarysearchform.is_submitted():
        # Get cards by text
        cardtext = librarysearchform.cardtext.data
        if cardtext:
            parameters += 1
            cards_by_cardtext = get_library_by_cardtext(cardtext)
            match_by_category.append(cards_by_cardtext)

        # Get cards by trait
        trait = librarysearchform.trait.data
        if trait:
            parameters += 1
            cards_by_trait = get_library_by_trait(trait)
            match_by_category.append(cards_by_trait)

        # Get cards by type
        cardtype = librarysearchform.cardtype.data
        if cardtype != 'ANY':
            parameters += 1
            cards_by_cardtype = get_library_by_cardtype(cardtype)
            match_by_category.append(cards_by_cardtype)

        # Get cards by disciplines
        discipline = librarysearchform.discipline.data
        if discipline != 'ANY':
            parameters += 1
            cards_by_discipline = get_library_by_discipline(discipline)
            match_by_category.append(cards_by_discipline)

        # Get cards by title
        title = librarysearchform.title.data
        if title != 'ANY':
            parameters += 1
            cards_by_title = get_library_by_title(title)
            match_by_category.append(cards_by_title)

        # Get cards by sect
        sect = librarysearchform.sect.data
        if sect != 'ANY':
            parameters += 1
            cards_by_sect = get_library_by_sect(sect)
            match_by_category.append(cards_by_sect)

        # Get cards by clan
        clan = librarysearchform.clan.data
        if clan != 'ANY':
            parameters += 1
            cards_by_clan = get_library_by_clan(clan)
            match_by_category.append(cards_by_clan)

        # Get cards by blood cost
        blood = librarysearchform.blood.data
        if blood != 'ANY':
            moreless = librarysearchform.bloodmoreless.data
            parameters += 1
            cards_by_blood = get_library_by_blood(blood, moreless)
            match_by_category.append(cards_by_blood)

        # Get cards by pool cost
        pool = librarysearchform.pool.data
        if pool != 'ANY':
            moreless = librarysearchform.poolmoreless.data
            parameters += 1
            cards_by_pool = get_library_by_pool(pool, moreless)
            match_by_category.append(cards_by_pool)

        # Get overall matches & total
        if parameters == 0:
            flash('CHOOSE AT LEAST ONE PARAMETER')
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
                flash('NO CARDS FOUND')

    return render_template('library.html',
                           searchform=librarysearchform,
                           cards=parsed_library_cards,
                           total=total)
