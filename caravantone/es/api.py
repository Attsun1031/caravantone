# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from .base import normalize

es = Elasticsearch()


def suggest(index, text, fuzziness=2):
    """call suggest es"""
    text = normalize(text)
    key = '{}-suggest'.format(index)
    completion_condition = {'field': 'suggest', 'fuzzy': {'fuzziness': fuzziness, 'unicode_aware': True}}
    response = es.suggest({key: {'text': text, 'completion': completion_condition}}, index=index)
    return response[key][0]['options']
