# -*- coding: utf-8 -*-

from caravantone.dao import Artist as ArtistDao, db_session, commit_with_fallback


class Artist(object):

    def __init__(self, name, freebase_topic_id=None, source=None, suspend_commit=True):
        self.__name = name
        self.__freebase_topic_id = freebase_topic_id
        if source:
            self.__source = source
        else:
            self.__source = ArtistDao(name=name, freebase_topic_id=freebase_topic_id)
            db_session.add(self.__source)
            if not suspend_commit:
                commit_with_fallback(db_session)

    @property
    def id(self):
        return self.__source.id

    @classmethod
    def find(cls, artist_id):
        artist = ArtistDao.query.get(artist_id)
        return cls._map(artist)

    @classmethod
    def _map(cls, source):
        return cls(source.name, source.freebase_topic_id, source=source)


find = Artist.find
