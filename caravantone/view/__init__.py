# -*- coding: utf-8 -*-


def configure(app):
    """configure all views"""
    from .error import configure as error_configure
    from .index import configure as index_configure
    from .login import configure as login_configure
    from .user import configure as user_configure
    from .artist import configure as artists_configure
    from .contents import configure as contents_configure

    error_configure(app)
    index_configure(app)
    login_configure(app)
    user_configure(app)
    artists_configure(app)
    contents_configure(app)
