# -*- coding: utf-8 -*-
from flask import redirect, request, session

from caravantone import app
from caravantone.model.oauth import generate_authorization_url, authorize_access, Provider
from caravantone.model.user import sign_up_with_oauth


@app.route('/login/twitter')
def twitter():
    return redirect(generate_authorization_url(Provider.twitter)[0])


@app.route('/login/twitter/authorize')
def twitter_authorize():
    tokens = authorize_access(Provider.twitter, request.url)
    user = sign_up_with_oauth(tokens.get('oauth_token'), tokens.get('oauth_token_secret'),
                              Provider.twitter.type_num, tokens.get('screen_name'))
    if user:
        # recreate session
        _ = session.pop('usre_id', None)
        session['user_id'] = user.id
        return redirect('/user')
    else:
        # TODO: redirect and show errors
        raise Exception()


@app.route('/login/hatena')
def hatena():
    return redirect(generate_authorization_url(Provider.hatena)[0])


@app.route('/login/hatena/authorize')
def hatena_authorize():
    tokens = authorize_access(Provider.hatena, request.url)
    return ','.join([tokens.get('oauth_token'), tokens.get('oauth_token_secret')])
