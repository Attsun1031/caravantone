# -*- coding: utf-8 -*-
import zenhan
from caravantone.exception import CaravantoneException


_trim_words = ('the ', 'a ')


def normalize(word):
    word = zenhan.z2h(word.lower(), zenhan.ASCII).strip()
    for t_word in _trim_words:
        if word.startswith(t_word):
            return word.lstrip(t_word)
    else:
        return word


class ESDoc(object):
    """document of elasticsearch"""

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
        return [normalize(self.__raw_input)]

    def to_dict(self):
        return {'input': self.__inputs, 'output': self.__output, 'payload': self.__payloads}
