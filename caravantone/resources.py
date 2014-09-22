# -*- coding: utf-8 -*-
from caravantone.model.artist import Artist as ArtistModel
from caravantone.model.user import User as UserModel
from caravantone.repository import artist_repository, user_repository
from caravantone.es.artist_suggestion import suggest_artist


def link(parent, child):
    parent[child.__name__] = child
    child.__parent__ = parent


class RootResource(object):

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


class ArtistResource(object):

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


class UserResource(object):

    def __init__(self, key):
        self.__name__ = self.key = key

    def retrieve(self):
        return user_repository.find_by_id(self.key)

    def delete(self):
        user_repository.delete_by_id(self.key)

    def add_artist(self, user, name, freebase_topic_id=None):
        # TODO: userはuser_factoryでこのインスタンス生成時に渡すようにしたい。
        artist = artist_repository.find_by_freebase_topic_id(freebase_topic_id)

        if not artist:
            artist = ArtistModel(name=name, freebase_topic_id=freebase_topic_id)
        user.check_artists(artist)
        user_repository.save(user)
        return artist


users_resource = UsersResource()


def users_factory(request):
    return users_resource


# TODO: aritsts APIをリソースで引けるようにする。
# http://zaiste.net/2013/12/building_a_restful_api_with_pyramid_resource_and_traversal/
# http://www.slideshare.net/aodag/pyramid-39068836
# http://pelican.aodag.jp/20140205-pyramid-controller-style.html
# http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/traversal.html
# http://docs.pylonsproject.jp/projects/pyramid-doc-ja/en/latest/narr/resources.html
# http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/hybrid.html
