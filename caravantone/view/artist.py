# -*- coding: utf-8 -*-
from flask import request, jsonify
from caravantone.view.util import require_login, jsonify_list
from caravantone.model.artist import Artist
from caravantone.es.artist_suggestion import suggest_artist
from caravantone.repository import artist_repository, user_repository


@require_login
def create(user):
    """create new artist data

    :param user: current user
    :return: Response
    """
    artist = artist_repository.find_by_freebase_topic_id(request.form.get('freebase_topic_id'))

    if not artist:
        artist = Artist(name=request.form.get('name'), freebase_topic_id=request.form.get('freebase_topic_id'))
    user.check_artists(artist)
    user_repository.save(user)

    return jsonify(name=artist.name)


@require_login
def suggest(user):
    """suggest artist name

    :param user: current user
    :return: Response
    """
    name = request.args.get('name', '')
    artists = suggest_artist(name)
    return jsonify_list([{'name': artist.name, 'id': artist.artist_id} for artist in artists])


def configure(app):
    app.route("/artists", methods=['POST'])(create)
    app.route("/artists/suggest", methods=['GET'])(suggest)

