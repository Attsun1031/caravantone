# -*- coding: utf-8 -*-


def configure(app):
    """configure all views"""
    from .index import configure as index_configure
    from .login import configure as login_configure
    from .artist import configure as artists_configure

    index_configure(app)
    login_configure(app)
    artists_configure(app)
