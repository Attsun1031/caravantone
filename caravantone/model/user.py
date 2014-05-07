# -*- coding: utf-8 -*-

from sqlalchemy.orm import load_only
from caravantone.dao import UserCheckedArtist, OauthToken, User as UserDao, db_session, commit_with_fallback


_load_oauth_token_with_only_private_key = OauthToken.query.options(load_only("user_id", "provider_type"))
def sign_up_with_oauth(token, secret, provider_type, name, profile=None, suspend_commit=False):
    """register both oauth_token and user.
     if oauth_token has already exist, return the user id.

    :param str token: access_token
    :param str secret: access_secret
    :param int provider_type: provider number
    :param str name: user name
    :param str profile: user profile
    :return: user id
    :rtype: int
    """
    conditions = (OauthToken.access_token == token,
                  OauthToken.access_secret == secret,
                  OauthToken.provider_type == provider_type)
    oauth_token = _load_oauth_token_with_only_private_key.filter(*conditions).first()

    if oauth_token:
        return oauth_token.user_id

    else:
        new_user = sign_up(name, profile=profile)
        new_oauth_token = OauthToken(access_token=token, access_secret=secret,
                                     provider_type=provider_type, user=new_user)
        db_session.add(new_oauth_token)
        if not suspend_commit:
            commit_with_fallback(db_session)
        return new_user.id


def sign_up(name, profile=None):
    """register new user

    :param name: user name
    :param profile: user profile
    :return: user
    :rtype: UserDao
    """
    user = UserDao(name=name, profile=profile)
    db_session.add(user)
    return user


class User(object):

    def __init__(self, name, profile=None, source=None, suspend_commit=True):
        self.__name = name
        self.__profile = profile
        if source:
            self.__source = source
        else:
            self.__source = UserDao(name=name, profile=profile)
            db_session.add(self.__source)
            if not suspend_commit:
                commit_with_fallback(db_session)

    @property
    def id(self):
        return self.__source.id

    def add_artists_to_stream(self, artists, suspend_commit=False):
        """add artists to my stream.

        :param [Artist] or Artist artists: artists (both one object and collection is acceptable)
        """
        if not isinstance(artists, (list, tuple)):
            artists = [artists]
        db_session.add_all([UserCheckedArtist(user_id=self.__source.id, artist_id=a.id) for a in artists])
        if not suspend_commit:
            commit_with_fallback(db_session)

    @classmethod
    def find(cls, user_id):
        user = UserDao.query.get(user_id)
        return cls._map(user)

    @classmethod
    def _map(cls, source):
        return cls(source.name, source.profile, source=source)


find = User.find
