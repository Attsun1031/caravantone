# -*- coding: utf-8 -*-
from flask import request, jsonify
from caravantone.view.util import require_login
from caravantone.external.youtube import search as search_from_youtube


@require_login
def search(user):
    """search resource by keyword

    :param user: current user
    :return: Response
    """
    keyword = request.args['keyword']
    next_page_token = request.args.get('next_page_token')
    search_result = search_from_youtube(keyword, next_page_token=next_page_token)
    items = [{'url': v.url, 'title': v.title, 'published_at': v.published_at} for v in search_result.items]
    return jsonify({'items': items, 'next_page_token': search_result.next_page_token})


def configure(app):
    app.route("/contents/search", methods=['GET'])(search)
