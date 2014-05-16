# -*- coding: utf-8 -*-
from flask import request, session, jsonify, abort
from caravantone.model.artist import Artist
from caravantone.repository import artist_repository, user_repository


def create():
    artist = artist_repository.find_by_freebase_topic_id(request.form.get('freebase_topic_id'))
    if not artist:
        artist = Artist(name=request.form.get('name'), freebase_topic_id=request.form.get('freebase_topic_id'))
    user = user_repository.find_by_id(session['user_id'])
    if not user:
        abort(400, 'illegal session state')
    user.check_artists(artist)
    user_repository.save(user)

    return jsonify(name=artist.name)


def configure(app):
    app.route("/artists", methods=['POST'])(create)
