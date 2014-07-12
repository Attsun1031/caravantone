# -*- coding: utf-8 -*-
from flask import request
from caravantone.view.util import require_login, jsonify_list
from caravantone.external.youtube import search as search_from_youtube


@require_login
def search(user):
    """search resource by keyword

    :param user: current user
    :return: Response
    """
    keyword = request.args['keyword']
    videos = [{'url': v.url, 'title': v.title} for v in search_from_youtube(keyword)]
    return jsonify_list(videos)


def configure(app):
    app.route("/contents/search", methods=['GET'])(search)
