# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.static import static_view
s_view = static_view('caravantone:static', use_subpath=True)


def includeme(config):
    config.add_route('login', '/login')
    config.scan('.view.login')

    # static view
    config.add_route('static', '/*subpath')
    config.add_view('caravantone.s_view', route_name='static')


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')
    config.add_jinja2_search_path('caravantone:templates', name='.html')
    config.include('.')

    return config.make_wsgi_app()
