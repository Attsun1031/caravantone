# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.static import static_view
s_view = static_view('caravantone:static', use_subpath=True)


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('static', '/*subpath')
    config.add_view('caravantone.s_view', route_name='static')

    return config.make_wsgi_app()
