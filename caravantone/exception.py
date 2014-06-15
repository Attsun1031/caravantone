# -*- coding: utf-8 -*-


class CaravantoneException(Exception):
    """Base exception class for this app"""

    default_code = 500

    def __init__(self, *args, **kwargs):
        errors = kwargs.pop('errors', None)
        code = kwargs.pop('code', self.default_code)
        super(CaravantoneException, self).__init__(*args, **kwargs)
        self.__errors = errors
        self.__code = code

    @property
    def code(self):
        return self.__code

    @property
    def errors(self):
        return self.__errors

