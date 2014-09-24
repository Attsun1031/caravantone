# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPUnauthorized, HTTPNotFound
from pyramid.view import view_config
from caravantone.es.base import ESException


# @app.errorhandler(ESException)
# def handle_es_exception(error):
#     response = jsonify({'error': error.errors})
#     response.status_code = error.code
#     return response


# @app.errorhandler(Exception)
# def handle_value_error(error):
#     if app.config['DEBUG']:
#         raise error
#     else:
#         response = jsonify({'error': 'Unknown error has occurred. {}'.format(str(error))})
#         response.status_code = 500
#         return response


@view_config(context=HTTPUnauthorized, renderer='json')
def e401(exc, request):
    request.response.status = exc.status
    return {'exc': str(exc), 'name': 'unauthorized'}


@view_config(context=HTTPNotFound, renderer='json')
def e404(exc, request):
    request.response.status = exc.status
    return {'exc': str(exc), 'name': 'notfound'}
