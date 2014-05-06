# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)
app.config.from_object('caravantone.config.Config')


if __name__ == "__main__":
    import caravantone.view as view
    view.configure(app)
    app.debug = app.config['DEBUG']
    app.run(host=app.config['HOST'], port=app.config['PORT'])
