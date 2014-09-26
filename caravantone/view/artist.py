# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.httpexceptions import exception_response

from caravantone.resources import ArtistsResource, ArtistResource
from caravantone.view.util import require_login


# Resourceを使ってREST APIを定義してみる
@view_config(route_name='artists', context=ArtistsResource, renderer='json', request_method='POST',
             decorator=require_login)
def create(context, request):
    artist = context.create(request.params['name'])
    if artist:
        request.response.status = '201 Created'
        return {'name': artist.name, 'id': artist.id}
    else:
        raise exception_response(500)


@view_config(route_name='artists', context=ArtistResource, renderer='json', request_method='GET',
             decorator=require_login)
def get(context, request):
    artist = context.retrieve()
    if artist:
        return {'name': artist.name}
    else:
        raise exception_response(404)


@view_config(route_name='artists', context=ArtistResource, renderer='json', request_method='DELETE',
             decorator=require_login)
def delete(context, request):
    context.delete()
    request.response.status = '204 No Content'


@view_config(route_name='artists', context=ArtistsResource, renderer='json', request_method='GET',
             name='suggest', decorator=require_login)
def suggest(context, request):
    return context.suggest(request.params['name'])
