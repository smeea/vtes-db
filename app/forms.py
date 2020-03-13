from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from wtforms import SelectMultipleField, SelectField
from wtforms.widgets import ListWidget, CheckboxInput, TableWidget, html_params, HTMLString
from markupsafe import Markup, escape
import re
# from wtforms.validators import Required


class DisciplineWidget(object):
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = []
        for subfield in field:
            d = re.match(r'<label .*>(\w+)</label>', str(subfield.label))
            dis = d.group(1)
            html.append(
                "<div>%s <img src='static/img/disciplines/%s.gif' height=24/></div>"
                % (subfield(), dis))
        return Markup("".join(html))


class CryptForm(FlaskForm):

    cardtext = StringField('Card Text')
    trait = SelectMultipleField('Text Trait',
                                option_widget=CheckboxInput(),
                                widget=ListWidget(prefix_label=False))

    disciplines = SelectMultipleField('Disciplines',
                                      option_widget=CheckboxInput(),
                                      widget=DisciplineWidget())

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
