from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import SelectMultipleField, SelectField
from wtforms.widgets import CheckboxInput, html_params
from markupsafe import Markup, escape

from wtforms import PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, DataRequired
from app.models import User

import re


class DisciplineClanWidget(object):
    def __call__(self, field, **kwargs):
        html = []
        i = True
        for subfield in field:
            if i is True:
                i = False
                html.append(
                    '<div name="discipline-checkbox" class="discipline-container js-discipline-container" style="display: none;">'
                )
                html.append(
                    '<div class="discipline-button-holder js-discipline-button-holder"></div>'
                )
                html.append('<label class="discipline-base-label" %s>' %
                            html_params(for_=subfield.id, **kwargs))
                html.append(
                    '<input class="d-none discipline-base js-discipline-base" type="checkbox" %s>'
                    % html_params(name=field.name,
                                  value=subfield._value(),
                                  id=subfield.id,
                                  **kwargs))
                html.append(
                    '<img src="static/img/disciplines/%s.gif" height="34">' %
                    subfield._value())
                html.append('</label>')
            else:
                i = True
                html.append('<label class="discipline-superior-label" %s>' %
                            html_params(for_=subfield.id, **kwargs))
                html.append(
                    '<input class="d-none discipline-superior js-discipline-superior" type="checkbox" %s>'
                    % html_params(name=field.name,
                                  value=subfield._value(),
                                  id=subfield.id,
                                  **kwargs))
                html.append(
                    '<img src="static/img/disciplines/%ss.gif" height="40">' %
                    subfield._value().lower())
                html.append('</label>')
                html.append('</div>')

        return Markup("".join(html))


class VirtuesWidget(object):
    def __call__(self, field, **kwargs):
        html = []
        for subfield in field:
            html.append('<div class="virtue-container" style:"display: none">')
            html.append('<label class="virtue-base-label" %s>' %
                        html_params(for_=subfield.id, **kwargs))
            html.append(
                '<input class="d-none virtue-base" type="checkbox" %s>' %
                html_params(name=field.name,
                            value=subfield._value(),
                            id=subfield.id,
                            **kwargs))
            html.append(
                '<img src="static/img/disciplines/%s.gif" height="33">' %
                subfield._value())
            html.append('</label>')
            html.append('</div>')
        return Markup("".join(html))


class TitleWidget(object):
    def __call__(self, field, **kwargs):
        html = []
        i = 0
        html.append('<div class="form-group col-7">')
        for subfield in field:
            if i == 7:
                html.append('</div>')
                html.append('<div class="form-group col-5">')
                i = 0
            i += 1
            input = "<input class='mr-2 custom-control-input' type='checkbox' %s>" % html_params(
                name=field.name,
                id=subfield.id,
                value=subfield._value(),
                **kwargs)
            label = "<label class='mr-2 custom-control-label' %s>%s</label>" % (
                html_params(name=field.name, for_=subfield.id, **
                            kwargs), subfield.label.text)
            html.append(
                "<div class=\"mr-2 custom-control custom-checkbox\">%s %s</div>"
                % (input, label))
        html.append('</div>')
        return Markup("".join(html))


class GroupWidget(object):
    def __call__(self, field, **kwargs):
        html = []
        for subfield in field:
            input = "<input class='mr-1 custom-control-input' type='checkbox' %s>" % html_params(
                name=field.name,
                id=subfield.id,
                value=subfield._value(),
                **kwargs)
            label = "<label class='mr-0 custom-control-label' %s>%s</label>" % (
                html_params(name=field.name, for_=subfield.id, **
                            kwargs), subfield.label.text)
            html.append(
                "<div class=\"ml-2 custom-control custom-checkbox\">%s %s</div>"
                % (input, label))
        return Markup("".join(html))


class TraitWidget(object):
    def __call__(self, field, **kwargs):
        html = []
        i = 0
        html.append('<div class="form-group col-7">')
        for subfield in field:
            if i == 9:
                html.append('</div>')
                html.append('<div class="col-5">')
                i = 0
            i += 1
            input = "<input class='mr-2 custom-control-input' type='checkbox' %s>" % html_params(
                name=field.name,
                id=subfield.id,
                value=subfield._value(),
                **kwargs)
            label = "<label class='mr-2 custom-control-label' %s>%s</label>" % (
                html_params(name=field.name, for_=subfield.id, **
                            kwargs), subfield.label.text)
            html.append(
                "<div class=\"mr-2 custom-control custom-checkbox\">%s %s</div>"
                % (input, label))
        html.append('</div>')
        return Markup("".join(html))


class SingleSelect(object):
    def __init__(self, id='select'):
        self.id = id

    def __call__(self, field, **kwargs):
        html = [
            "<select %s>" % html_params(
                name=field.name, class_='custom-select', id=self.id, **kwargs)
        ]
        for val, label, selected in field.iter_choices():
            html.append(self.render_option(val, label, selected))
        html.append("</select>")
        return Markup("".join(html))

    @classmethod
    def render_option(cls, value, label, selected, **kwargs):
        options = dict(kwargs, value=value)
        if selected:
            options["selected"] = True
        return Markup("<option %s>%s</option>" %
                      (html_params(**options), escape(label)))


class ClanSelect(object):
    def __init__(self, id='select'):
        self.id = id

    def __call__(self, field, **kwargs):
        # Add 'data-live-search=true' after select for live-search in form box
        html = [
            "<select data-style='btn-secondary' data-width=%s %s>" %
            ('100%',
             html_params(
                 name=field.name, class_='selectpicker', id=self.id, **kwargs))
        ]
        for val, label, selected in field.iter_choices():
            html.append(self.render_option(val, label, selected))
        html.append("</select>")
        return Markup("".join(html))

    @classmethod
    def render_option(cls, value, label, selected, **kwargs):
        options = dict(kwargs, value=value)
        if selected:
            options["selected"] = True
        if label != 'ANY':
            filename = re.sub('[\\W]', '', label).lower()
            imgurl = 'static/img/clans/' + filename + '.gif'
            img_margin_tag = '<span style="display:inline-block; width: 45px; text-align: center">'
            return Markup(
                "<option data-content='<div>%s<img height=24 src=%s></span> %s</div>'>%s</option>"
                % (escape(img_margin_tag), escape(imgurl), escape(label),
                   escape(value)))
        else:
            return Markup(
                "<option data-content='<div class=pl-1>%s</div>'>%s</option>" %
                (escape(label), escape(value)))


class DisciplineLibrarySelect(object):
    def __init__(self, id='select'):
        self.id = id

    def __call__(self, field, **kwargs):
        # Add 'data-live-search=true' after select for live-search in form box
        html = [
            "<select data-style='btn-secondary' data-width=%s %s>" %
            ('100%',
             html_params(
                 name=field.name, class_='selectpicker', id=self.id, **kwargs))
        ]
        for val, label, selected in field.iter_choices():
            html.append(self.render_option(val, label, selected))
        html.append("</select>")
        return Markup("".join(html))

    @classmethod
    def render_option(cls, value, label, selected, **kwargs):
        options = dict(kwargs, value=value)
        if selected:
            options["selected"] = True
        if label != 'ANY':
            # Hack around Visionary and Visceratika
            if label == 'Thanatosis':
                imgurl = 'static/img/disciplines/' + 'thn' + '.gif'
            elif label == 'Vision':
                imgurl = 'static/img/disciplines/' + 'visi' + '.gif'
            else:
                imgurl = 'static/img/disciplines/' + label[:3].lower() + '.gif'
            img_margin_tag = '<span style="display:inline-block; width: 45px; text-align: center">'
            return Markup(
                "<option data-content='<div>%s<img height=24 src=%s></span> %s</div>'>%s</option>"
                % (escape(img_margin_tag), escape(imgurl), escape(label),
                   escape(value)))
        else:
            return Markup(
                "<option data-content='<div class=pl-1>%s</div>'>%s</option>" %
                (escape(label), escape(value)))


class TypeSelect(object):
    def __init__(self, id='select'):
        self.id = id

    def __call__(self, field, **kwargs):
        html = [
            "<select data-style='btn-secondary' data-width=%s %s>" %
            ('100%',
             html_params(
                 name=field.name, class_='selectpicker', id=self.id, **kwargs))
        ]
        for val, label, selected in field.iter_choices():
            html.append(self.render_option(val, label, selected))
        html.append("</select>")
        return Markup("".join(html))

    @classmethod
    def render_option(cls, value, label, selected, **kwargs):
        options = dict(kwargs, value=value)
        if selected:
            options["selected"] = True
        if label != 'ANY':
            filename = re.sub('[\\W]', '', label).lower()
            imgurl = 'static/img/types/' + filename + '.gif'
            img_margin_tag = '<span style="display:inline-block; width: 45px; text-align: center">'
            return Markup(
                "<option data-content='<div>%s<img height=24 src=%s></span> %s</div>'>%s</option>"
                % (escape(img_margin_tag), escape(imgurl), escape(label),
                   escape(label)))
        else:
            return Markup(
                "<option data-content='<div class=ml-1>%s</div>'>%s</option>" %
                (escape(label), escape(label)))


class CryptSearchForm(FlaskForm):
    cardtext = StringField('Card Text')
    disciplines = SelectMultipleField('Disciplines',
                                      option_widget=CheckboxInput(),
                                      widget=DisciplineClanWidget())
    virtues = SelectMultipleField('Virtues',
                                  option_widget=CheckboxInput(),
                                  widget=VirtuesWidget())
    votes = SelectField('Votes', widget=SingleSelect(id='votes'))
    clan = SelectField('Clan', widget=ClanSelect(id='clan'))
    sect = SelectField('Sect', widget=SingleSelect(id='sect'))
    titles = SelectMultipleField('Titles',
                                 option_widget=CheckboxInput(),
                                 widget=TitleWidget())
    capacitymoreless = SelectField('Capacity More-Less',
                                   widget=SingleSelect(id='capacitymoreless'))
    capacity = SelectField('Capacity', widget=SingleSelect(id='capacity'))
    group = SelectMultipleField('Group',
                                option_widget=CheckboxInput(),
                                widget=GroupWidget())
    trait = SelectMultipleField('Text Trait',
                                option_widget=CheckboxInput(),
                                widget=TraitWidget())
    submit = SubmitField('Search')


class LibrarySearchForm(FlaskForm):
    cardtext = StringField('Card Text')
    trait = SelectMultipleField('Text Trait',
                                option_widget=CheckboxInput(),
                                widget=TraitWidget())
    discipline = SelectField('Disciplines',
                             widget=DisciplineLibrarySelect(id='discipline'))
    cardtype = SelectField('Card Type', widget=TypeSelect(id='cardtype'))
    clan = SelectField('Clan', widget=ClanSelect(id='clan'))
    sect = SelectField('Sect', widget=SingleSelect(id='sect'))
    title = SelectField('Title', widget=SingleSelect(id='title'))
    poolmoreless = SelectField('Pool More-Less',
                               widget=SingleSelect(id='poolmoreless'))
    pool = SelectField('Pool Cost', widget=SingleSelect(id='pool'))
    bloodmoreless = SelectField('Blood More-Less',
                                widget=SingleSelect(id='bloodmoreless'))
    blood = SelectField('Blood Cost', widget=SingleSelect(id='blood'))
    submit = SubmitField('Search')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(),
                                          EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
