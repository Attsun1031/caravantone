# -*- coding: utf-8 -*-
from flask.json import dumps
from werkzeug.datastructures import MultiDict
from wtforms import Form


class ValidationError(Exception):
    def __init__(self, *args, **kwargs):
        errors = kwargs.pop('errors', None)
        super(ValidationError, self).__init__(*args, **kwargs)
        self.__errors = errors

    @property
    def errors(self):
        return self.__errors


def _get_method(attr):
    attr_name = '_{}'.format(attr)
    def fget(self):
        return getattr(self, attr_name)
    return fget


def _set_method(attr):
    attr_name = '_{}'.format(attr)
    def fset(self, value):
        setattr(self, attr_name, value)
    return fset


class FieldAccessorMeta(type):
    def __new__(cls, name, bases, namespace, **kwargs):
        form_class = namespace['_form_class']
        for name in dir(form_class):
            if name.startswith('_'):
                continue
            unbound_field = getattr(form_class, name)
            if not hasattr(unbound_field, '_formfield'):
                continue

            getter = '_get_{}'.format(name)
            setter = '_set_{}'.format(name)
            fget = namespace[getter] if getter in namespace else _get_method(name)
            fset = namespace[setter] if setter in namespace else _set_method(name)
            namespace[name] = property(fget, fset)
        return type.__new__(cls, name, bases, dict(namespace))


class Entity(metaclass=FieldAccessorMeta):

    _form_class = Form

    def __init__(self, **kwargs):
        form = self._form_class(**kwargs)
        if not form.validate():
            raise ValidationError(dumps(form.errors), errors=form.errors)
        form.populate_obj(self)

    def __eq__(self, other):
        if self.id is other.id:
            return True
        else:
            return False


class ValueObject(metaclass=FieldAccessorMeta):

    _form_class = Form

    def __init__(self, **kwargs):
        form = self._form_class(MultiDict(kwargs))
        if not form.validate():
            raise ValidationError(dumps(form.errors), errors=form.errors)
        form.populate_obj(self)

    def __eq__(self, other):
        for f in self._form_class._unbound_fields:
            if getattr(self, f[0]) != getattr(other, f[0]):
                return False
        else:
            return True


class Field(object):
    def __init__(self, name, default=None, mandatory=False, primary=False, fget=None):
        self.name = name
        self.primary = primary
        self.default = default
        self.mandatory = mandatory
        self.fget = fget


