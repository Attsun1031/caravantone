# -*- coding: utf-8 -*-


def _get_method(attr):
    attr_name = '_{}'.format(attr)
    def fget(self):
        return getattr(self, attr_name)
    return fget


class FieldAccessorMeta(type):
    def __new__(cls, name, bases, namespace, **kwargs):
        for f in namespace['__fields__']:
            fget = _get_method(f.name) if f.fget is None else f.fget
            namespace[f.name] = property(fget)
        return type.__new__(cls, name, bases, dict(namespace))


class Entity(metaclass=FieldAccessorMeta):

    __fields__ = []

    def __init__(self, **kwargs):
        for f in self.__fields__:
            if f.mandatory and f.name not in kwargs:
                raise ValueError('field "" is missed'.format(f.name))
            setattr(self, '_{}'.format(f.name), kwargs.get(f.name, f.default))

    def __eq__(self, other):
        # Is it non-sense to compare other values except ID...?
        for f in self.__fields__:
            if getattr(self, f.name) != getattr(other, f.name):
                return False
        else:
            return True


class ValueObject(metaclass=FieldAccessorMeta):

    __fields__ = []

    def __init__(self, **kwargs):
        for f in self.__fields__:
            if f.mandatory and f.name not in kwargs:
                raise ValueError('field "" is missed'.format(f.name))
            setattr(self, '_{}'.format(f.name), kwargs.get(f.name, f.default))

    def __eq__(self, other):
        for f in self.__fields__:
            if getattr(self, f.name) != getattr(other, f.name):
                return False
        else:
            return True


class Field(object):
    def __init__(self, name, primary=False, default=None, mandatory=False, fget=None):
        self.name = name
        self.primary = primary
        self.default = default
        self.mandatory = mandatory
        self.fget = fget


