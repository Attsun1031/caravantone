# -*- coding: utf-8 -*-
from functools import wraps

from pyramid.httpexceptions import HTTPUnauthorized


def require_login(f):
    """decorate function that require login session."""
    @wraps(f)
    def _wrapper(context, request):
        if not request.user:
            raise HTTPUnauthorized('Require login session')
        return f(context, request)
    return _wrapper

'''
def _default_error_handler(form):
    abort(400, 'Illegal params: {}'.format(dumps(form.errors)))


def validate(FormClass, on_error=_default_error_handler):
    """validate request values by FormClass instance

    :param FormClass:
    :param on_error: function that handle errors. This function need to accept one argument as form.
    :return: decorator
    """
    def _validate(f):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            form = FormClass(request.args if request.method == 'GET' else request.form)

            if not form.validate():
                on_error(form)
            else:
                kwargs['form'] = form
                return f(*args, **kwargs)
        return _wrapper
    return _validate


def jsonify_list(array):
    """jsonify list object

    :param list array: jsonifed
    :return: Rseponse
    """
    indent = None
    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] and not request.is_xhr:
        indent = 2
    return current_app.response_class(dumps(array, indent=indent), mimetype='application/json')
'''
