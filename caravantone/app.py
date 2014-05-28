# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)
app.config.from_object('caravantone.config.Config')

# cannot use ssl with py3
# see: https://github.com/mitsuhiko/werkzeug/issues/434
"""
from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('/usr/local/ssl/server.key')
context.use_certificate_file('/usr/local/ssl/server.crt')
"""

if __name__ == "__main__":
    import caravantone.view as view
    view.configure(app)
    app.debug = app.config['DEBUG']
    #app.run(host=app.config['HOST'], port=app.config['PORT'], ssl_context=context)
    app.run(host=app.config['HOST'], port=app.config['PORT'])
