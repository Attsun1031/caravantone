# -*- coding: utf-8 -*-
from caravantone import app


def index():
    return app.send_static_file('index.html')


def configure(app):
    app.route("/")(index)
