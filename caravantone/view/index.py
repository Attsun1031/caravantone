# -*- coding: utf-8 -*-


def configure(app):
    @app.route("/index")
    def index():
        return "index World!"
