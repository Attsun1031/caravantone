# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)
app.config.from_object('caravantone.config.Config')
app.debug = app.config['DEBUG']

# cannot use ssl with py3
# see: https://github.com/mitsuhiko/werkzeug/issues/434
"""
from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('/usr/local/ssl/server.key')
context.use_certificate_file('/usr/local/ssl/server.crt')
"""

