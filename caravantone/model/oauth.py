# -*- coding: utf-8 -*-

from enum import Enum
from requests_oauthlib import OAuth1Session


secret = None

class Provider(object):
    """oauth provider
    """

    def __init__(self, name, request_token_uri, authorization_uri, access_token_uri,
                 callback_uri=None):
        self.name = name
        self.request_token_uri = request_token_uri
        self.authorization_uri = authorization_uri
        self.access_token_uri = access_token_uri
        self.callback_uri = callback_uri

    @property
    def consumer_key(self):
        return ''

    @property
    def consumer_secret(self):
        return ''


class ProviderType(Enum):
    """ type for oauth provider
    """

    twitter = Provider(name='twitter',
                       request_token_uri='https://api.twitter.com/oauth/request_token',
                       authorization_uri='https://api.twitter.com/oauth/authenticate',
                       access_token_uri='https://api.twitter.com/oauth/access_token',
                       callback_uri='http://192.168.56.101:5000/login/oauth')


def generate_authorization_url(provider_type):
    """generate url for authorization

    :param ProviderType provider_type: type of provider
    :rtype: (str, dict)
    :return: (url for authorization, request token)
    """
    provider = provider_type.value
    session = OAuth1Session(provider.consumer_key,
                            client_secret=provider.consumer_secret,
                            callback_uri=provider.callback_uri)
    res = session.fetch_request_token(provider.request_token_uri)
    secret = res.get('oauth_token_secret')
    return session.authorization_url(provider.authorization_uri, res.get('oauth_token')), res


def authorize_access(provider_type, authorization_response_url):
    """authorize access to provider

    :param ProviderType provider_type: type of provider
    :param str authorization_response_url: url from authorization request
    :rtype: dict
    :return: access token
    """
    provider = provider_type.value
    session = OAuth1Session(provider.consumer_key,
                            client_secret=provider.consumer_secret)
    res = session.parse_authorization_response(authorization_response_url)
    session = OAuth1Session(provider.consumer_key,
                            client_secret=provider.consumer_secret,
                            resource_owner_key=res.get('oauth_token'),
                            resource_owner_secret=secret,
                            verifier=res.get('oauth_verifier'))
    return session.fetch_access_token(provider.access_token_uri)
