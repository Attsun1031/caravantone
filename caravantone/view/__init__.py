# -*- coding: utf-8 -*-

from .index import configure as index_configure


def configure(app):
    '''configure all views'''
    @app.route("/")
    def hello():
        return "Hello World!"
    index_configure(app)
