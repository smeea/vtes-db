#!/usr/bin/env python3

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
    disciplines = StringField('Disciplines')
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

    submit = SubmitField('Go')


class LibraryForm(FlaskForm):
    cardtext = StringField('Card Text')
    discipline = SelectField('Disciplines')
    cardtype = SelectField('Card Type')
    clan = SelectField('Clan')
    sect = SelectField('Sect')
    title = SelectField('Titles')
    submit = SubmitField('Go')
