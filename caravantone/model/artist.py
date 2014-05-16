# -*- coding: utf-8 -*-
from caravantone.model.base import Entity, Field


class Artist(Entity):

    __fields__ = (Field('id'), Field('name', mandatory=True), Field('freebase_topic_id'))
