# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.static import static_view

from sqlalchemy import engine_from_config

from .dao import Base, db_session


s_view = static_view('caravantone:static', use_subpath=True)


def includeme(config):
    config.add_route('login', '/login/user')
    config.scan('.view.login')

    # static view
    config.add_route('static', '/*subpath')
    config.add_view('caravantone.s_view', route_name='static')


def configure_database(settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    db_session.configure(bind=engine)
    Base.metadata.bind = engine
    Base.query = db_session.query_property()


def main(global_config, **settings):
    configure_database(settings)

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')
    config.add_jinja2_search_path('caravantone:templates', name='.html')
    config.include('.')

    return config.make_wsgi_app()
