# -*- coding: utf-8 -*-
from sqlalchemy.orm.attributes import instance_state
from caravantone.repository.base import RepositoryBase, MapperBase, DBSupport
from caravantone.repository.artist import ArtistMapper
from caravantone.dao import UserRecord, OauthTokenRecord
from caravantone.model.oauth import OauthToken


class UserMapper(MapperBase):

    def __init__(self, artist_mapper, oauth_token_mapper):
        self.__artist_mapper = artist_mapper
        self.__oauth_token_mapper= oauth_token_mapper

    def data2model(self, data):
        from caravantone.model.user import User
        unloaded = instance_state(data).unloaded
        checked_artists = None
        if 'checked_artists' not in unloaded:
            checked_artists = [self.__artist_mapper.data2model(artist) for artist in data.checked_artists]
        oauth_tokens = None
        if 'oauth_tokens' not in unloaded:
            oauth_tokens = [self.__oauth_token_mapper.data2model(token) for token in data.oauth_tokens]
        return User(id=data.id, name=data.name, profile=data.profile, checked_artists=checked_artists,
                    oauth_tokens=oauth_tokens, password=data.password)

    def model2data(self, model):
        if model.id is not None:
            data = UserRecord.query.get(model.id)
            data.name = model.name
            data.profile = model.profile
            data.password = model.password
        else:
            data = UserRecord(name=model.name, profile=model.profile, password=model.password)

        # update relations if they are loaded
        if model._checked_artists is not None:
            data.checked_artists = [self.__artist_mapper.model2data(d) for d in model.checked_artists]
        if model._oauth_tokens is not None:
            data.oauth_tokens = [self.__oauth_token_mapper.model2data(d) for d in model.oauth_tokens]

        return data


class OauthTokenMapper(MapperBase):
    def data2model(self, data):
        return OauthToken(access_token=data.access_token,
                          access_secret=data.access_secret,
                          provider_type=data.provider_type)

    def model2data(self, model):
        return OauthTokenRecord(access_token=model.access_token,
                                access_secret=model.access_secret,
                                provider_type=model.provider.type_num)


class UserRepository(DBSupport, RepositoryBase):

    _dao_class = UserRecord

    _mapper = UserMapper(ArtistMapper(), OauthTokenMapper())

    def find_by_oauth_token(self, token, secret, provider_type, one=True):
        conditions = (OauthTokenRecord.access_token == token,
                      OauthTokenRecord.access_secret == secret,
                      OauthTokenRecord.provider_type == provider_type)
        data = UserRecord.query.join(OauthTokenRecord).filter(*conditions)
        if one:
            obj = data.first()
            if obj is not None:
                return self._mapper.data2model(obj)
            else:
                return None
        else:
            return map(self._mapper.data2model, data.all())

    def find_by_name(self, name):
        data = UserRecord.query.filter_by(name=name).first()
        if data:
            return self._mapper.data2model(data)
        else:
            return None

    def get_oauth_tokens(self, user_id):
        return map(self._mapper.data2model, OauthTokenRecord.query.filter(OauthTokenRecord.user_id == user_id))

    def _after_save(self, model, data):
        model._id = data.id
