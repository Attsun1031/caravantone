# -*- coding: utf-8 -*-
from pyramid.view import view_config

from .util import require_login
from caravantone.resources import UserResource


@view_config(route_name="users", context=UserResource, request_method='GET', renderer='my_page.html')
@require_login
def get(context, request, user):
    u = context.retrieve()
    return {'user': {'name': u.name, 'id': u.id}}


@view_config(route_name="users", context=UserResource, request_method='POST', renderer='json', name='artists')
@require_login
def create(context, request, user):
    """create new artist data

    :param user: current user
    :return: Response
    """
    artist = context.add_artist(user, request.params['name'], request.params.get('freebase_topic_id'))
    return dict(name=artist.name)


