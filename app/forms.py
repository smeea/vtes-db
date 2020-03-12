from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from wtforms import SelectMultipleField, SelectField
from wtforms.widgets import ListWidget, CheckboxInput
# from wtforms.validators import Required


class CryptForm(FlaskForm):
    cardtext = StringField('Card Text')
    trait = SelectMultipleField('Text Trait',
                                option_widget=CheckboxInput(),
                                widget=ListWidget(prefix_label=False))
    disciplines = SelectMultipleField('Disciplines',
                                      option_widget=CheckboxInput(),
                                      widget=ListWidget(prefix_label=False))
    votes = SelectField('Votes')
    clan = SelectField('Clan')
    sect = SelectField('Sect')
    titles = SelectMultipleField('Titles',
                                 option_widget=CheckboxInput(),
                                 widget=ListWidget(prefix_label=False))
    capacitymoreless = SelectField('Capacity More-Less')
    capacity = SelectField('Capacity')
    group = SelectMultipleField('Group',
                                option_widget=CheckboxInput(),
                                widget=ListWidget(prefix_label=False))

    submit = SubmitField('Search')


class LibraryForm(FlaskForm):
    cardtext = StringField('Card Text')
    trait = SelectMultipleField('Text Trait',
                                option_widget=CheckboxInput(),
                                widget=ListWidget(prefix_label=False))
    discipline = SelectField('Disciplines')
    cardtype = SelectField('Card Type')
    clan = SelectField('Clan')
    sect = SelectField('Sect')
    title = SelectField('Titles')
    submit = SubmitField('Search')
    poolmoreless = SelectField('Pool More-Less')
    pool = SelectField('Pool Cost')
    bloodmoreless = SelectField('Blood More-Less')
    blood = SelectField('Blood Cost')
