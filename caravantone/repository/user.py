# -*- coding: utf-8 -*-
from caravantone.repository.base import Repository, MapperBase
from caravantone.repository.strategy import DBStrategy
from caravantone.repository.artist import ArtistMapper
from caravantone.dao import UserRecord
from caravantone.model.user import User


class UserRepository(Repository):

    def __init__(self):
        self.__db_strategy = DBStrategy(UserRecord, UserMapper(ArtistMapper()))

    def find_by_id(self, ident):
        return self.__db_strategy.find_by_id(ident)

    def save(self, model, flush=True):
        self.__db_strategy.save(model, flush=flush)


class UserMapper(MapperBase):

    def __init__(self, artist_mapper):
        self.__artist_mapper = artist_mapper

    def data2model(self, data):
        artists = [self.__artist_mapper.data2model(d) for d in data.checked_artists]
        return User(id=data.id, name=data.name, profile=data.profile, checked_artists=artists)

    def model2data(self, model):
        artist_records = [self.__artist_mapper.model2data(d) for d in model.checked_artists]
        if model.id is not None:
            data = UserRecord.query.get(model.id)
        else:
            data = UserRecord(name=model.name, profile=model.profile)
        data.checked_artists = artist_records
        return data
