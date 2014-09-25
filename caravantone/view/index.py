# -*- coding: utf-8 -*-
from pyramid.view import view_config


@view_config(route_name="top", renderer='index.html')
def index(context, request):
    return {}
