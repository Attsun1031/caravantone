# -*- coding: utf-8 -*-
from caravantone.repository.base import RepositoryBase, MapperBase, DBSupport
from caravantone.repository.artist import ArtistMapper
from caravantone.dao import UserRecord, OauthTokenRecord
from caravantone.model.user import User


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


class UserRepositoryBase(DBSupport, RepositoryBase):

    _dao_class = UserRecord

    _mapper = UserMapper(ArtistMapper())
    #_load_oauth_token_with_only_private_key = OauthTokenRecord.query.options(load_only("user_id", "provider_type"))
