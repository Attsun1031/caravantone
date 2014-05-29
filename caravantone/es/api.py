# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch

es = Elasticsearch()


def suggest(index, text, fuzziness=2):
    """call suggest es"""
    key = '{}-suggest'.format(index)
    completion_condition = {'field': 'suggest', 'fuzzy': {'fuzziness': fuzziness, 'unicode_aware': True}}
    response = es.suggest({key: {'text': text, 'completion': completion_condition}}, index='music')
    return response[key][0]['options']
