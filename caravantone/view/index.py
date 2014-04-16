# -*- coding: utf-8 -*-


def index():
    return "index World!"

def configure(app):
    app.route("/index")(index)
