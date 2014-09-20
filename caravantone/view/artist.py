# -*- coding: utf-8 -*-
from pyramid.view import view_config

from caravantone.view.util import require_login
from caravantone.model.artist import Artist
from caravantone.es.artist_suggestion import suggest_artist
from caravantone.repository import artist_repository, user_repository


@view_config(route_name="artists", request_method='POST', renderer='json')
@require_login
def create(context, request, user):
    """create new artist data

    :param user: current user
    :return: Response
    """
    artist = artist_repository.find_by_freebase_topic_id(request.params.get('freebase_topic_id'))

    if not artist:
        artist = Artist(name=request.params.get(r'name'), freebase_topic_id=request.params.get('freebase_topic_id'))
    user.check_artists(artist)
    user_repository.save(user)

    return dict(name=artist.name)


@view_config(route_name='artists_suggest', request_method='GET', renderer='json')
@require_login
def suggest(context, request, user):
    """suggest artist name

    :param user: current user
    :return: Response
    """
    name = request.params.get('name', '')
    artists = suggest_artist(name)
    return dict(result=[{'name': artist.name, 'id': artist.artist_id} for artist in artists])


from caravantone.resources import PathResource, ArtistsResource, ArtistResource
@view_config(context=PathResource, renderer='json')
def path(context, request):
    return {'value': 'Resource', 'type': str(type(context))}


# Resourceを使ってREST APIを定義してみる
@view_config(route_name='r_artists', context=ArtistsResource, renderer='json', request_method='POST')
def r_create(context, request):
    artist = context.create(request.params['name'])
    return {'name': artist.name, 'id': artist.id}


@view_config(route_name='r_artists', context=ArtistResource, renderer='json', request_method='GET')
def r_get(context, request):
    return {'key': context.key}


# nameの実験
@view_config(route_name='r_artists', context=ArtistResource, renderer='json', request_method='GET', name='edit')
def r_edit(context, request):
    return {'edit': context.key}
