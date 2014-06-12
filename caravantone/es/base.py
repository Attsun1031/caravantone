# -*- coding: utf-8 -*-
from caravantone.exception import CaravantoneException


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
        return [self.__raw_input]

    def to_dict(self):
        return {'input': self.__inputs, 'output': self.__output, 'payload': self.__payloads}
