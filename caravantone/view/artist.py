# -*- coding: utf-8 -*-
from flask import request, jsonify
from wtforms import Form, TextField, validators
from caravantone.view.util import require_login, validate
from caravantone.model.artist import Artist
from caravantone.repository import artist_repository, user_repository


class CreateForm(Form):
    name = TextField('name', [validators.InputRequired()])
    freebase_topic_id = TextField('freebase_topic_id', [validators.InputRequired()])


@validate(CreateForm)
@require_login
def create(user, form):
    artist = artist_repository.find_by_freebase_topic_id(request.form.get('freebase_topic_id'))
    if not artist:
        artist = Artist(name=request.form.get('name'), freebase_topic_id=request.form.get('freebase_topic_id'))
    user.check_artists(artist)
    user_repository.save(user)

    return jsonify(name=artist.name)


def configure(app):
    app.route("/artists", methods=['POST'])(create)
