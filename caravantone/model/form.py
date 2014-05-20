# -*- coding: utf-8 -*-
from wtforms import FieldList
from wtforms.validators import StopValidation


class AggregateField(FieldList):
    def populate_obj(self, obj, name):
        if not self.entries:
            setattr(obj, name, None)
        else:
            super(AggregateField, self).populate_obj(obj, name)


class TypeOf(object):
    field_flags = ('typeof', )

    def __init__(self, tp, message=None):
        self.type = tp
        self.message = message

    def __call__(self, form, field):
        if not isinstance(field.data, self.type):
            if self.message is None:
                message = field.gettext('This field should be instance of {}.'.format(self.type))
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)

