# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.exceptions import NotFound

from caravantone.view.util import require_login
from caravantone.resources import ContentsResource


# TODO: pyramidに書き換える

# @app.route("/contents", methods=['GET'])
# @require_login
# def index_contents(user):
#     """Search contents by keyword
#
#     :param user: current user
#     :return: Response
#     """
#     if not 'keyword' in request.args:
#         return render_template('contents_search.html', title='コンテンツ検索')
#
#     keyword = request.args['keyword']
#     next_page_token = request.args.get('next_page_token')
#     search_result = search_from_youtube(keyword, next_page_token=next_page_token)
#     items = [{'url': v.url, 'title': v.title, 'published_at': _format_published_at(v.published_at)} for v in
#              search_result.items]
#     return jsonify({'items': items, 'next_page_token': search_result.next_page_token})

@view_config(route_name='contents_search', renderer='contents_search.html', decorator=require_login)
def index(request):
    return {}


@view_config(route_name='contents', context=ContentsResource, renderer='json', request_method='GET',
             decorator=require_login)
def get(context, request):
    keyword = request.params['keyword']
    next_page_token = request.params.get('next_page_token')
    items = context.find(keyword, next_page_token)
    if items:
        return items
    else:
        raise NotFound('No item found. keyword: {keyword}, next_page_token: {next_page_token}'.format_map(locals()))


def _format_published_at(value):
    """Strip time info from publishedAt value.

    >>> _format_published_at('2014-01-01T12:40:10Z')
    '2014-01-01'
    """
    return value[:10]
