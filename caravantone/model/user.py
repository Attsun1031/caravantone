# -*- coding: utf-8 -*-
from caravantone.dao import OauthTokenRecord, UserRecord as UserDao, db_session, commit_with_fallback
from caravantone.model.base import Entity, Field
from caravantone.repository import user_repository


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

    user = user_repository.find_by_oauth_token(token, secret, provider_type)

    if user:
        return user.id

    else:
        new_user = sign_up(name, profile=profile)
        new_oauth_token = OauthTokenRecord(access_token=token, access_secret=secret,
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


class User(Entity):

    def __get_artists(self):
        from caravantone.repository import artist_repository
        if self._checked_artists is None:
            self._checked_artists = list(artist_repository.find_by_user_id(self.id))
        return self._checked_artists

    def __get_oauth_tokens(self):
        if self._oauth_tokens is None:
            self._oauth_tokens = list(user_repository.get_oauth_tokens(self.id))
        return self._oauth_tokens

    __fields__ = (Field('id', mandatory=True), Field('name', mandatory=True), Field('profile'),
                  Field('checked_artists', fget=__get_artists), Field('oauth_tokens', fget=__get_oauth_tokens))

    def check_artists(self, artists):
        """add artists to my stream.

        :param [Artist] or Artist artists: artists (both one object and collection is acceptable)
        """
        if not isinstance(artists, (list, tuple)):
            artists = [artists]
        self.checked_artists.extend(artists)
