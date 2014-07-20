# -*- coding: utf-8 -*-
from caravantone import app


@app.route('/')
def index():
    return app.send_static_file('index.html')
