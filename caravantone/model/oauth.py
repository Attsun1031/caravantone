# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
from wtforms import Form, StringField, IntegerField, validators, Field

from caravantone.model.base import ValueObject
from caravantone.dao import redis_session


class Provider:
    """oauth provider"""

    def __init__(self, provider_name, type_num, request_token_uri, authorization_uri, access_token_uri,
                 callback_path):
        """constructor

        :param provider_name: name of provider
        :param request_token_uri: uri for request token
        :param authorization_uri: uri for authorization
        :param access_token_uri: uri for access token
        :param callback_path: callback path after authorization
        """
        self.consumer_key = None
        self.consumer_secret = None
        self.provider_name = provider_name
        self.type_num = type_num
        self.request_token_uri = request_token_uri
        self.authorization_uri = authorization_uri
        self.access_token_uri = access_token_uri
        self.callback_path = callback_path

    def get_callback_uri(self, host_url):
        if host_url.endswith('/'):
            host_url = host_url[:-1]
        return '{}{}'.format(host_url, self.callback_path)


twitter = Provider('twitter', 1,
                   'https://api.twitter.com/oauth/request_token',
                   'https://api.twitter.com/oauth/authenticate',
                   'https://api.twitter.com/oauth/access_token',
                   '/login/twitter/authorize')

hatena = Provider('hatena', 2,
                  'https://www.hatena.com/oauth/initiate',
                  'https://www.hatena.ne.jp/oauth/authorize',
                  'https://www.hatena.com/oauth/token',
                  '/login/hatena/authorize')

provider_map = {twitter.type_num: twitter, hatena.type_num: hatena}


def includeme(config):
    settings = config.get_settings()
    secret = settings['secret']
    twitter.consumer_key = secret['twitter']['key']
    twitter.consumer_secret = secret['twitter']['secret']

    hatena.consumer_key = secret['hatena']['key']
    hatena.consumer_secret = secret['hatena']['secret']


def generate_authorization_url(provider, host_url):
    """generate url for authorization

    :param ProviderType provider: type of provider
    :rtype: (str, dict)
    :return: (url for authorization, request token)
    """
    session = OAuth1Session(provider.consumer_key,
                            client_secret=provider.consumer_secret,
                            callback_uri=provider.get_callback_uri(host_url))
    res = session.fetch_request_token(provider.request_token_uri)
    token = res['oauth_token']
    redis_session.set(_generate_key(provider.provider_name, token), res['oauth_token_secret'])
    return session.authorization_url(provider.authorization_uri, token), res


def authorize_access(provider, oauth_token, oauth_verifier):
    """authorize access to provider

    :param ProviderType provider: type of provider
    :param str authorization_response_url: url from authorization request
    :rtype: dict
    :return: access token
    """
    secret = redis_session.get(_generate_key(provider.provider_name, oauth_token))
    session = OAuth1Session(provider.consumer_key,
                            client_secret=provider.consumer_secret,
                            resource_owner_key=oauth_token,
                            resource_owner_secret=secret,
                            verifier=oauth_verifier)
    return session.fetch_access_token(provider.access_token_uri)


def _generate_key(provider_name, key):
    return '{}:{}'.format(provider_name, key)


class OauthTokenForm(Form):
    access_token = StringField(validators=[validators.DataRequired()])
    access_secret = StringField(validators=[validators.DataRequired()])
    provider_type = IntegerField()
    provider = Field()


class OauthToken(ValueObject):

    _form_class = OauthTokenForm

    def __init__(self, **kwargs):
        super(OauthToken, self).__init__(**kwargs)
        if self._provider is None and self._provider_type is None:
            raise ValueError('provider_type or provider_type is required')
        if self._provider is None:
            self._provider = provider_map[self._provider_type]
