# -*- coding: utf-8 -*-
from pyramid.request import Request
from pyramid.decorator import reify
from pyramid.security import authenticated_userid

from caravantone.repository import user_repository


class UserRetainRequetMixIn(object):

    @reify
    def user(self):
        """
        Curretn login user
        """
        auth = authenticated_userid(self)
        if not auth:
            return None
        uid, _ = auth.split(':')
        user = user_repository.find_by_id(uid)
        if not user:
            return None
        else:
            return user


class CaravantoneRequest(UserRetainRequetMixIn, Request):
    """Base request class for caravantone"""

