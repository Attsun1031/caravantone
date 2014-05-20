# -*- coding: utf-8 -*-
from flask import request, jsonify
from caravantone.view.util import require_login
from caravantone.model.artist import Artist
from caravantone.repository import artist_repository, user_repository


@require_login
def create(user):
    artist = artist_repository.find_by_freebase_topic_id(request.form.get('freebase_topic_id'))

    if not artist:
        artist = Artist(name=request.form.get('name'), freebase_topic_id=request.form.get('freebase_topic_id'))
    user.check_artists(artist)
    user_repository.save(user)

    return jsonify(name=artist.name)


def configure(app):
    app.route("/artists", methods=['POST'])(create)
