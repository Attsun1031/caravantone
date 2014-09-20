# -*- coding: utf-8 -*-
from configparser import ConfigParser

from pyramid.config import Configurator
from pyramid.static import static_view
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config

from .dao import Base, db_session
from .resources import root_factory


s_view = static_view('caravantone:static', use_subpath=True)


def includeme(config):
    config.add_route('login', '/login/user')
    config.add_route('login_test', '/login/test')
    config.add_route('login_hatena', '/login/hatena')
    config.add_route('login_hatena_authorize', '/login/hatena/authorize')
    config.add_route('artists', '/artists')
    config.add_route('artists_suggest', '/artists/suggest')
    # config.add_route('resource', '/resource')
    config.add_route('r_artists', '/r/*traverse', factory=root_factory)
    config.scan('.view.login')
    config.scan('.view.artist')

    # static view
    # resourceと競合する。
    # config.add_route('static', '/*subpath')
    # config.add_view('caravantone.s_view', route_name='static')


def configure_database(settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    db_session.configure(bind=engine)
    Base.metadata.bind = engine
    Base.query = db_session.query_property()


def main(global_config, **settings):
    configure_database(settings)

    config = Configurator(settings=settings)

    # secrets
    secret = ConfigParser()
    secret.read(config.get_settings()['secret'])
    config.add_settings({'secret': secret})

    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')
    config.add_jinja2_search_path('caravantone:templates', name='.html')
    config.include('.')
    config.include('.model.oauth')

    # security
    config.set_authentication_policy(AuthTktAuthenticationPolicy('__attsun__'))
    config.set_authorization_policy(ACLAuthorizationPolicy())

    return config.make_wsgi_app()
