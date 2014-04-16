# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
from flask import redirect


params = None

def twitter():
    # TODO: unauthorizedになってしまうので、トークン設定を見なおしてみる。
    # http://d.hatena.ne.jp/speg03/20091019/1255957580
    session = OAuth1Session('',
                            client_secret='',
                            callback_uri='http://192.168.56.101:5000/login/oauth')
    res = session.post('https://api.twitter.com/oauth/request_token')
    params = dict([p.split('=') for p in res.text.split('&')])
    return redirect('https://api.twitter.com/oauth/authenticate?oauth_token={}'.format(params['oauth_token']))

def oauth():
    return 'hello'

def configure(app):
    app.route('/login/twitter')(twitter)
    app.route('/login/oauth')(oauth)

