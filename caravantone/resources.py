# -*- coding: utf-8 -*-
from logging import getLogger
from caravantone.model.artist import Artist as ArtistModel
from caravantone.model.user import User as UserModel
from caravantone.repository import artist_repository, user_repository
from caravantone.es.artist_suggestion import suggest_artist
from caravantone.external.youtube import search as search_from_youtube


logger = getLogger(__name__)


def link(parent, child):
    parent[child.__name__] = child
    child.__parent__ = parent


class RootResource:

    __name__ = __parent__ = None


class ArtistsResource(RootResource):

    def __getitem__(self, item):
        rsc = ArtistResource(item)
        rsc.__parent__ = self
        return rsc

    def create(self, name):
        new_artist = ArtistModel(name=name)
        artist_repository.save(new_artist)
        return new_artist

    def suggest(self, name):
        artists = suggest_artist(name)
        return dict(result=[{'name': artist.name, 'id': artist.artist_id} for artist in artists])


class ArtistResource:

    def __init__(self, key):
        self.__name__ = self.key = key

    def retrieve(self):
        return artist_repository.find_by_id(self.key)

    def delete(self):
        artist_repository.delete_by_id(self.key)


artists_resource = ArtistsResource()


def artists_factory(request):
    return artists_resource


#
# Users
#
class UsersResource(RootResource):

    def __getitem__(self, item):
        rsc = UserResource(item)
        rsc.__parent__ = self
        return rsc

    def create(self, name):
        new_user = UserModel(name=name)
        user_repository.save(new_user)
        return new_user


class UserResource:

    def __init__(self, key):
        self.__name__ = self.key = key

    def retrieve(self):
        return user_repository.find_by_id(self.key)

    def delete(self):
        user_repository.delete_by_id(self.key)

    def add_artist(self, user, name, freebase_topic_id=None):
        artist = artist_repository.find_by_freebase_topic_id(freebase_topic_id)

        if not artist:
            artist = ArtistModel(name=name, freebase_topic_id=freebase_topic_id)
        user.check_artists(artist)
        user_repository.save(user)
        return artist


users_resource = UsersResource()


def users_factory(request):
    return users_resource


#
# Contents
#

class ContentsResource(RootResource):
    """Resource of contents collection"""

    def __getitem__(self, item):
        rsc = UserResource(item)
        rsc.__parent__ = self
        return rsc

    def find(self, keyword, next_page_token=None):
        search_result = search_from_youtube(keyword, next_page_token=next_page_token)
        logger.info('Search from youtubue. count: {:d}'.format(len(search_result)))
        items = [{'url': v.url, 'title': v.title, 'published_at': self._format_published_at(v.published_at)} for v in
                 search_result.items]
        return items

    def _format_published_at(self, value):
        """Strip time info from publishedAt value.

        >>> _format_published_at('2014-01-01T12:40:10Z')
        '2014-01-01'
        """
        return value[:10]


contents_resource = ContentsResource()


def contents_factory(request):
    return contents_resource
