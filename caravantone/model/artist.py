# -*- coding: utf-8 -*-
from wtforms import Form, StringField, IntegerField, validators
from caravantone.model.base import Entity


class ArtistForm(Form):
    id = IntegerField()
    name = StringField(validators=[validators.DataRequired()])
    freebase_topic_id = StringField()


class Artist(Entity):

    _form_class = ArtistForm
