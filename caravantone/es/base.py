# -*- coding: utf-8 -*-
import re

import zenhan

import caravantone.wordutil as wordutil
from caravantone.exception import CaravantoneException

_normalize_regex = r'[・ 　]'


def normalize(text):
    text = zenhan.h2z(text, zenhan.KANA)
    text = zenhan.z2h(text, zenhan.ASCII|zenhan.DIGIT)
    text = _normalize_regex.sub('', text)
    text = wordutil.kana2hira(text)
    return text


class ESDoc(object):

    index_type = 'caravantone'


class ESException(CaravantoneException):
    pass


class FailedToPutDoc(ESException):
    pass


class Suggest(object):
    def __init__(self, input, output=None, payloads=None):
        self.__raw_input = input
        self.__output = output if output is not None else input
        self.__payloads = payloads

        self.__inputs = self._make_inputs()

    def _make_inputs(self):
        result = [normalize(self.__raw_input)]
        reading = wordutil.get_reading(result)
        if reading != result[0]:
            result.append(reading)

    def to_dict(self):
        return {'input': self.__inputs, 'output': self.__output, 'payload': self.__payloads}
