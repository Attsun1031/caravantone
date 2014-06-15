# -*- coding: utf-8 -*-


def configure(app):
    """configure all views"""
    from .error import configure as error_configure
    from .index import configure as index_configure
    from .login import configure as login_configure
    from .artist import configure as artists_configure

    error_configure(app)
    index_configure(app)
    login_configure(app)
    artists_configure(app)
