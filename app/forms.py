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
        i = 0
        html.append('<table>')
        for subfield in field:
            d = re.match(r'<label .*>(\w+)</label>', str(subfield.label))
            dis = d.group(1)
            if len(dis) == 3:
                height = '24'
            else:
                height = '27'
            if i < 1:
                html.append('<tr>')
            i += 1
            html.append(
                "<td><span>%s <img src='static/img/disciplines/%s.gif' height=%s/></span></td>"
                % (subfield(), dis, height))
            if i == 6:
                html.append('</tr>')
                i = 0
        html.append('</table>')
        return Markup("".join(html))


class TitleWidget(object):
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = []
        i = 0
        html.append('<table>')
        html.append('<tr>')
        html.append('<td valign=top>')
        for subfield in field:
            i += 1
            html.append(
                "<span style='font-size:x-small' align='top'>%s %s</span><br>"
                % (subfield(), subfield.label))
            if i == 5:
                html.append('</td>')
                html.append('<td valign=top>')
                i = 0
        html.append('</td>')
        html.append('</tr>')
        html.append('</table>')
        return Markup("".join(html))


class GroupWidget(object):
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = []
        html.append('<table>')
        html.append('<tr>')
        for subfield in field:
            html.append(
                "<td><span style='font-size:x-small' align='top'>%s %s</span></td>"
                % (subfield(), subfield.label))
        html.append('</tr>')
        html.append('</table>')
        return Markup("".join(html))


class TraitWidget(object):
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = []
        i = 0
        html.append('<table>')
        html.append('<tr>')
        html.append('<td valign=top>')
        for subfield in field:
            i += 1
            html.append(
                "<span style='font-size:x-small' align='top'>%s %s</span><br>"
                % (subfield(), subfield.label))
            if i == 6:
                html.append('</td>')
                html.append('<td valign=top>')
                i = 0
        html.append('</td>')
        html.append('</tr>')
        html.append('</table>')
        return Markup("".join(html))


class CryptForm(FlaskForm):

    cardtext = StringField('Card Text')
    trait = SelectMultipleField('Text Trait',
                                option_widget=CheckboxInput(),
                                widget=TraitWidget())

    disciplines = SelectMultipleField('Disciplines',
                                      option_widget=CheckboxInput(),
                                      widget=DisciplineWidget())

    votes = SelectField('Votes')
    clan = SelectField('Clan')
    sect = SelectField('Sect')
    titles = SelectMultipleField('Titles',
                                 option_widget=CheckboxInput(),
                                 widget=TitleWidget())
    capacitymoreless = SelectField('Capacity More-Less')
    capacity = SelectField('Capacity')
    group = SelectMultipleField('Group',
                                option_widget=CheckboxInput(),
                                widget=GroupWidget())

    submit = SubmitField('Search')


class LibraryForm(FlaskForm):
    cardtext = StringField('Card Text')
    trait = SelectMultipleField('Text Trait',
                                option_widget=CheckboxInput(),
                                widget=TraitWidget())
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
