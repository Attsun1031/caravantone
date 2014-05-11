# -*- coding: utf-8 -*-

from enum import Enum
from redis import StrictRedis
from requests_oauthlib import OAuth1Session

from caravantone.app import app
from caravantone.model.base import ValueObject, Field


def generate_authorization_url(provider):
    """generate url for authorization

    :param ProviderType provider: type of provider
    :rtype: (str, dict)
    :return: (url for authorization, request token)
    """
    session = OAuth1Session(provider.consumer_key,
                            client_secret=provider.consumer_secret,
                            callback_uri=provider.callback_uri)
    res = session.fetch_request_token(provider.request_token_uri)
    token = res['oauth_token']
    StrictRedis().set(_generate_key(provider.provider_name, token), res['oauth_token_secret'])
    return session.authorization_url(provider.authorization_uri, token), res


def authorize_access(provider, authorization_response_url):
    """authorize access to provider

    :param ProviderType provider: type of provider
    :param str authorization_response_url: url from authorization request
    :rtype: dict
    :return: access token
    """
    session = OAuth1Session(provider.consumer_key,
                            client_secret=provider.consumer_secret)
    res = session.parse_authorization_response(authorization_response_url)

    secret = StrictRedis().get(_generate_key(provider.provider_name, res['oauth_token']))
    session = OAuth1Session(provider.consumer_key,
                            client_secret=provider.consumer_secret,
                            resource_owner_key=res.get('oauth_token'),
                            resource_owner_secret=secret,
                            verifier=res.get('oauth_verifier'))
    return session.fetch_access_token(provider.access_token_uri)


def _generate_key(provider_name, key):
    return '{}:{}'.format(provider_name, key)


class Provider(Enum):
    """oauth provider
    """

    twitter = ('twitter', 1, 'https://api.twitter.com/oauth/request_token',
               'https://api.twitter.com/oauth/authenticate', 'https://api.twitter.com/oauth/access_token',
               '/login/twitter/authorize')

    hatena = ('hatena', 2, 'https://www.hatena.com/oauth/initiate',
              'https://www.hatena.ne.jp/oauth/authorize', 'https://www.hatena.com/oauth/token',
              '/login/hatena/authorize')

    def __init__(self, provider_name, type_num, request_token_uri, authorization_uri,  access_token_uri,  callback_path):
        """constructor

        :param provider_name: name of provider
        :param request_token_uri: uri for request token
        :param authorization_uri: uri for authorization
        :param access_token_uri: uri for access token
        :param callback_path: callback path after authorization
        """
        self.consumer_key = app.config.get('{}_CONSUMER_KEY'.format(provider_name.upper()))
        self.consumer_secret = app.config.get('{}_CONSUMER_SECRET'.format(provider_name.upper()))
        self.provider_name = provider_name
        self.type_num = type_num
        self.request_token_uri = request_token_uri
        self.authorization_uri = authorization_uri
        self.access_token_uri = access_token_uri

        domain = app.config['HOST']
        port = app.config['PORT']
        scheme = 'http'
        if port == 443:
            scheme = 'https'
        elif port != 80:
            domain = '{}:{:d}'.format(domain, port)
        self.callback_uri = '{}://{}{}'.format(scheme, domain, callback_path)


class OauthToken(ValueObject):

    __fields__ = (Field('access_token', mandatory=True), Field('access_secret', mandatory=True),
                  Field('provider_type'), Field('provider'))

    def __init__(self, **kwargs):
        super(OauthToken, self).__init__(**kwargs)
        if self._provider is None and self._provider_type is None:
            raise ValueError('provider_type or provider_type is required')
        if self._provider is None:
            valid_providers = [p for p in Provider if p.type_num == self._provider_type]
            if not valid_providers:
                raise ValueError('invalid provider_type: {}'.format(self._provider_type))
            self._provider = valid_providers[0]
