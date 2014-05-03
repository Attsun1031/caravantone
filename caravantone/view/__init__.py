# -*- coding: utf-8 -*-


def configure(app):
    from .index import configure as index_configure
    from .login import configure as login_configure

    '''configure all views'''
    @app.route("/")
    def hello():
        return "Hello World!"

    index_configure(app)
    login_configure(app)
