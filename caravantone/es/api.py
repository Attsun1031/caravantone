# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from wtforms import Form, StringField, validators
from .base import normalize, ESException

es = Elasticsearch()


class InvalidSuggestRequest(ESException):
    """Raised if Suggest request is invalid."""


class SuggestRequestForm(Form):
    text = StringField(validators=[validators.DataRequired(), validators.Length(max=50)])


def suggest(index, text, fuzziness=2):
    """call suggest es"""
    text = normalize(text)

    form = SuggestRequestForm(text=text)
    if not form.validate():
        raise InvalidSuggestRequest(errors=form.errors)

    if text == "white":
        raise ValueError

    key = '{}-suggest'.format(index)
    completion_condition = {'field': 'suggest', 'fuzzy': {'fuzziness': fuzziness, 'unicode_aware': True}}
    response = es.suggest({key: {'text': text, 'completion': completion_condition}}, index=index)
    return response[key][0]['options']
