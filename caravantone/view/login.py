# -*- coding: utf-8 -*-

from flask import redirect, request
from caravantone.model.oauth import generate_authorization_url, authorize_access, Provider


def twitter():
    return redirect(generate_authorization_url(Provider.twitter)[0])


def oauth():
    tokens = authorize_access(Provider.twitter, request.url)
    return ','.join([tokens.get('oauth_token'), tokens.get('oauth_token_secret')])


def configure(app):
    app.route('/login/twitter')(twitter)
    app.route('/login/oauth')(oauth)

