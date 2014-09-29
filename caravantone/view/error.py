# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPUnauthorized, HTTPNotFound
from pyramid.view import view_config


@view_config(context=HTTPUnauthorized, renderer='json')
def e401(exc, request):
    request.response.status = exc.status
    return {'exc': str(exc), 'name': 'unauthorized'}


@view_config(context=HTTPNotFound, renderer='json')
def e404(exc, request):
    request.response.status = exc.status
    return {'exc': str(exc), 'name': 'notfound'}
