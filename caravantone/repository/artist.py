# -*- coding: utf-8 -*-
from caravantone.repository.base import Repository, MapperBase
from caravantone.repository.strategy import DBStrategy
from caravantone.dao import ArtistRecord
from caravantone.model.artist import Artist


class ArtistRepository(Repository):

    def __init__(self):
        self.__db_strategy = DBStrategy(ArtistRecord, ArtistMapper())

    def find_by_id(self, ident):
        return self.__db_strategy.find_by_id(ident)

    def save(self, model, flush=True):
        self.__db_strategy.save(model, flush=flush)


class ArtistMapper(MapperBase):
    def data2model(self, data):
        return Artist(id=data.id, name=data.name, freebase_topic_id=data.freebase_topic_id)

    def model2data(self, model):
        if model.id is not None:
            data = ArtistRecord.query.get(model.id)
        else:
            data = ArtistRecord(name=model.name, freebase_topic_id=model.freebase_topic_id)
        return data
