# -*- coding: utf-8 -*-
from caravantone.repository.base import RepositoryBase, MapperBase, DBSupport
from caravantone.repository.artist import ArtistMapper
from caravantone.dao import UserRecord, OauthTokenRecord
from caravantone.model.user import User


class UserMapper(MapperBase):

    def __init__(self, artist_mapper):
        self.__artist_mapper = artist_mapper

    def data2model(self, data):
        return User(id=data.id, name=data.name, profile=data.profile)

    def model2data(self, model):
        if model.id is not None:
            data = UserRecord.query.get(model.id)
        else:
            data = UserRecord(name=model.name, profile=model.profile)
        if model._checked_artists is not None:
            # update if loaded
            data.checked_artists = [self.__artist_mapper.model2data(d) for d in model.checked_artists]
        return data


class UserRepository(DBSupport, RepositoryBase):

    _dao_class = UserRecord

    _mapper = UserMapper(ArtistMapper())

    _query_for_find_by_oauth_token = UserRecord.query.join(OauthTokenRecord)

    def find_by_oauth_token(self, token, secret, provider_type, one=True):
        conditions = (OauthTokenRecord.access_token == token,
                      OauthTokenRecord.access_secret == secret,
                      OauthTokenRecord.provider_type == provider_type)
        data = self._query_for_find_by_oauth_token.filter(*conditions)
        if not data:
            return None
        else:
            if one:
                return self._mapper.data2model(data.first())
            else:
                return [self._mapper.data2model(d) for d in data.all()]

    def extract_oauth_tokens(self, user_id):
        # TODO: implement
        pass
