# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.response import Response

from caravantone.view.util import require_login
from caravantone.model.user import authenticate
from caravantone.model.oauth import authorize_access, generate_authorization_url, hatena


@view_config(route_name='login')
def user(context, request):
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
def login_test(context, request, user):
    return Response(user.name)

# @app.route('/login/twitter')
# def twitter_oauth():
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


@view_config(route_name='login_hatena')
def hatena_oauth(request):
    return HTTPFound(location=generate_authorization_url(hatena, request.host_url)[0])


@view_config(route_name='login_hatena_authorize')
def hatena_authorize(request):
    tokens = authorize_access(hatena, request.params['oauth_token'], request.params['oauth_verifier'])
    return Response(','.join([tokens.get('oauth_token'), tokens.get('oauth_token_secret')]))
