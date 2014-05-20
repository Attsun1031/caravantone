# -*- coding: utf-8 -*-
from wtforms import Form, StringField, IntegerField, validators, Field

from caravantone.model.base import Entity
from caravantone.model.form import AggregateField, TypeOf
from caravantone.model.oauth import OauthToken
from caravantone.model.artist import Artist
from caravantone.repository import user_repository


def sign_up_with_oauth(token, secret, provider_type, name, profile=None):
    """register both oauth_token and user.
     if oauth_token has already exist, return the user id.

    :param str token: access_token
    :param str secret: access_secret
    :param int provider_type: provider number
    :param str name: user name
    :param str profile: user profile
    :return: user
    :rtype: User
    """
    user = user_repository.find_by_oauth_token(token, secret, provider_type)

    if user:
        return user
    else:
        new_user = User(name=name, profile=profile)
        new_oauth_token = OauthToken(access_token=token, access_secret=secret, provider_type=provider_type)
        new_user.authorize_oauth(new_oauth_token)
        user_repository.save(new_user)
        return new_user


class UserForm(Form):
    id = IntegerField()
    name = StringField(validators=[validators.DataRequired()])
    profile = StringField()
    checked_artists = AggregateField(Field(validators=[TypeOf(Artist)]))
    oauth_tokens = AggregateField(Field(TypeOf(OauthToken)))


class User(Entity):

    _form_class = UserForm

    def _get_checked_artists(self):
        from caravantone.repository import artist_repository
        if self._checked_artists is None:
            self._checked_artists = list(artist_repository.find_by_user_id(self.id))
        return self._checked_artists

    def _get_oauth_tokens(self):
        if self._oauth_tokens is None:
            self._oauth_tokens = list(user_repository.get_oauth_tokens(self.id))
        return self._oauth_tokens

    def check_artists(self, artists):
        """add artists to my stream.

        :param [Artist] or Artist artists: artists (both one object and collection is acceptable)
        """
        if not isinstance(artists, (list, tuple)):
            artists = [artists]
        self.checked_artists.extend(artists)

    def authorize_oauth(self, oauth):
        self.oauth_tokens.append(oauth)
