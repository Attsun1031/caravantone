# -*- coding: utf-8 -*-

from enum import Enum
from redis import StrictRedis
from requests_oauthlib import OAuth1Session


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

    twitter = ('twitter', 'https://api.twitter.com/oauth/request_token',
               'https://api.twitter.com/oauth/authenticate', 'https://api.twitter.com/oauth/access_token',
               'http://192.168.56.101:5000/login/twitter/authorize')

    hatena = ('hatena', 'https://www.hatena.com/oauth/initiate',
              'https://www.hatena.ne.jp/oauth/authorize', 'https://www.hatena.com/oauth/token',
              'http://192.168.56.101:5000/login/hatena/authorize')

    def __init__(self, provider_name, request_token_uri, authorization_uri,  access_token_uri,  callback_uri):
        """constructor

        :param provider_name: name of provider
        :param request_token_uri: uri for request token
        :param authorization_uri: uri for authorization
        :param access_token_uri: uri for access token
        :param callback_uri: callback uri after authorization
        """
        _redis_session = StrictRedis()

        self.consumer_key = _redis_session.get(_generate_key(provider_name, 'consumer_key'))
        self.consumer_secret = _redis_session.get(_generate_key(provider_name, 'consumer_secret'))
        self.provider_name = provider_name
        self.request_token_uri = request_token_uri
        self.authorization_uri = authorization_uri
        self.access_token_uri = access_token_uri
        self.callback_uri = callback_uri


