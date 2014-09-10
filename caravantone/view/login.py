# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.response import Response

from caravantone.view.util import require_login
from caravantone.model.user import authenticate


# @view_config(route_name='login', renderer='my_page.html')
@view_config(route_name='login')
def user(request):
    u = authenticate(request.POST.get('name'), request.POST.get('password'))
    if u:
        # recreate session
        auth = remember(request, '{:d}:{}'.format(u.id, u.name))
        response = HTTPFound(location='/login/test')
        response.headerlist.extend(auth)
        return response
    else:
        raise Exception('Failed to authenticate user')


@view_config(route_name='login_test')
@require_login
def login_test(request):
    return Response('OK')

# @app.route('/login/twitter')
# def twitter():
#     return redirect(generate_authorization_url(Provider.twitter)[0])
#
#
# @app.route('/login/twitter/authorize')
# def twitter_authorize():
#     tokens = authorize_access(Provider.twitter, request.url)
#     user = sign_up_with_oauth(tokens.get('oauth_token'), tokens.get('oauth_token_secret'),
#                               Provider.twitter.type_num, tokens.get('screen_name'))
#     if user:
#         # recreate session
#         _ = session.pop('usre_id', None)
#         session['user_id'] = user.id
#         return redirect('/user')
#     else:
#         # TODO: redirect and show errors
#         raise Exception()
#
#
# @app.route('/login/hatena')
# def hatena():
#     return redirect(generate_authorization_url(Provider.hatena)[0])
#
#
# @app.route('/login/hatena/authorize')
# def hatena_authorize():
#     tokens = authorize_access(Provider.hatena, request.url)
#     return ','.join([tokens.get('oauth_token'), tokens.get('oauth_token_secret')])
