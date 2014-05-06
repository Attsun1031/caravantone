# -*- coding: utf-8 -*-

from sqlalchemy.orm import load_only
from caravantone.dao import OauthToken, User, db_session, commit_with_fallback


_load_oauth_token_with_only_private_key = OauthToken.query.options(load_only("user_id", "provider_type"))
def sign_up_with_oauth(token, secret, provider_type, name, profile=None, suspend_commit=False):
    """register both oauth_token and user.
     if oauth_token has already exist, return the user id.

    :param str token: access_token
    :param str secret: access_secret
    :param int provider_type: provider number
    :param str name: user name
    :param str profile: user profile
    :param bool suspend_commit: suspend to call session.commit
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
        new_user = sign_up(name, profile=profile, suspend_commit=True)
        new_oauth_token = OauthToken(access_token=token, access_secret=secret,
                                     provider_type=provider_type, user=new_user)
        db_session.add(new_oauth_token)
        if not suspend_commit:
            commit_with_fallback(db_session)
        return new_user.id


def sign_up(name, profile=None, suspend_commit=False):
    """register new user

    :param name: user name
    :param profile: user profile
    :param suspend_commit: suspend to call session.commit
    :return: user
    :rtype: User
    """
    user = User(name=name, profile=profile)
    db_session.add(user)
    if not suspend_commit:
        commit_with_fallback(db_session)
    return user
