# -*- coding: utf-8 -*-
from flask import jsonify
from caravantone.es.base import ESException
from caravantone.app import app


@app.errorhandler(ESException)
def handle_es_exception(error):
    response = jsonify({'error': error.errors})
    response.status_code = error.code
    return response


@app.errorhandler(Exception)
def handle_value_error(error):
    if app.config['DEBUG']:
        raise error
    else:
        response = jsonify({'error': 'Unknown error has occurred. {}'.format(str(error))})
        response.status_code = 500
        return response
