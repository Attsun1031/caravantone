# -*- coding: utf-8 -*-
from functools import wraps
from flask import jsonify
from caravantone.es.base import ESException
from caravantone.app import app


error_handler_mapping = {}


def on_error(ex):
    """When Exception ex has raised, call decorated function by this.

    @on_error(ValueError)
    def on_value_error(error):
        return Response()

    :param ex: type of exception
    """
    def _on_error(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        error_handler_mapping[ex] = f
        return wrapper
    return _on_error


@on_error(ESException)
def handle_es_exception(error):
    response = jsonify({'error': error.errors})
    response.status_code = error.code
    return response


@on_error(Exception)
def handle_value_error(error):
    if app.config['DEBUG']:
        raise error
    else:
        response = jsonify({'error': 'Unknown error has occurred. {}'.format(str(error))})
        response.status_code = 500
        return response


def configure(app):
    for ex_type, callback in error_handler_mapping.items():
        app.errorhandler(ex_type)(callback)


