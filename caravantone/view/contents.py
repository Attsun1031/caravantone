# -*- coding: utf-8 -*-
from flask import request, jsonify, render_template

from caravantone import app
from caravantone.view.util import require_login
from caravantone.external.youtube import search as search_from_youtube


@app.route("/contents", methods=['GET'])
@require_login
def index_contents(user):
    """Search contents by keyword

    :param user: current user
    :return: Response
    """
    if not 'keyword' in request.args:
        return render_template('contents_search.html', title='コンテンツ検索')

    keyword = request.args['keyword']
    next_page_token = request.args.get('next_page_token')
    search_result = search_from_youtube(keyword, next_page_token=next_page_token)
    items = [{'url': v.url, 'title': v.title, 'published_at': _format_published_at(v.published_at)} for v in
             search_result.items]
    return jsonify({'items': items, 'next_page_token': search_result.next_page_token})


def _format_published_at(value):
    """Strip time info from publishedAt value.

    >>> _format_published_at('2014-01-01T12:40:10Z')
    '2014-01-01'
    """
    return value[:10]
