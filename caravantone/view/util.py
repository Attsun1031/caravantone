# -*- coding: utf-8 -*-
from functools import wraps
from flask import session, abort
from caravantone.repository import user_repository


def require_login(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):
        if 'user_id' not in session:
            abort(400, 'illegal session state')
        user = user_repository.find_by_id(session['user_id'])
        if not user:
            abort(400, 'illegal session state')
        kwargs['user'] = user
        return f(*args, **kwargs)
    return _wrapper

