# -*- coding: utf-8 -*-

from .base import ESDoc, Suggest, FailedToPutDoc
from .api import es


class Artist(ESDoc):
    """artist doc_type on elasticsearch"""

    index_type = 'caravantone'

    doc_type = 'artist'

    id_name = 'artist_id'

    def __init__(self, artist_id, name):
        self.__artist_id = artist_id
        self.__name = name

    @property
    def artist_id(self):
        return self.__artist_id

    @property
    def name(self):
        return self.__name

    @classmethod
    def suggest(cls, text):
        pass

    def update(self):
        suggest = Suggest(self.name, payloads={'artist_id': self.artist_id})
        result = es.index(index=self.index_type, doc_type=self.doc_type,
                          id=getattr(self, self.id_name),
                          body={'name': self.name, 'suggest': suggest.to_dict()})

        if not result['created']:
            raise FailedToPutDoc(str(result))
