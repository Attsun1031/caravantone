# -*- coding: utf-8 -*-

from flask import redirect, request
from caravantone.model.oauth import generate_authorization_url, authorize_access, Provider


def twitter():
    return redirect(generate_authorization_url(Provider.twitter)[0])


def twitter_authorize():
    tokens = authorize_access(Provider.twitter, request.url)
    return ','.join([tokens.get('oauth_token'), tokens.get('oauth_token_secret')])


def hatena():
    return redirect(generate_authorization_url(Provider.hatena)[0])


def hatena_authorize():
    tokens = authorize_access(Provider.hatena, request.url)
    return ','.join([tokens.get('oauth_token'), tokens.get('oauth_token_secret')])


def configure(app):
    app.route('/login/twitter')(twitter)
    app.route('/login/twitter/authorize')(twitter_authorize)
    app.route('/login/hatena')(hatena)
    app.route('/login/hatena/authorize')(hatena_authorize)

