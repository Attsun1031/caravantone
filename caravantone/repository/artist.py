# -*- coding: utf-8 -*-
from caravantone.repository.base import RepositoryBase, MapperBase, DBSupport
from caravantone.dao import ArtistRecord
from caravantone.model.artist import Artist


class ArtistMapper(MapperBase):
    def data2model(self, data):
        return Artist(id=data.id, name=data.name, freebase_topic_id=data.freebase_topic_id)

    def model2data(self, model):
        if model.id is not None:
            data = ArtistRecord.query.get(model.id)
        else:
            data = ArtistRecord(name=model.name, freebase_topic_id=model.freebase_topic_id)
        return data


class ArtistRepositoryBase(DBSupport, RepositoryBase):

    _dao_class = ArtistRecord

    _mapper = ArtistMapper()


