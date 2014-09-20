# -*- coding: utf-8 -*-
from caravantone.repository.base import RepositoryBase, MapperBase, DBSupport
from caravantone.dao import ArtistRecord, UserCheckedArtistRecord
from caravantone.model.artist import Artist


class ArtistMapper(MapperBase):
    def data2model(self, data):
        return Artist(id=data.id, name=data.name, freebase_topic_id=data.freebase_topic_id)

    def model2data(self, model):
        if model.id is not None:
            data = ArtistRecord.query.get(model.id)
            data.name = model.name
            data.freebase_topic_id = model.freebase_topic_id
        else:
            data = ArtistRecord(name=model.name, freebase_topic_id=model.freebase_topic_id)
        return data


class ArtistRepository(DBSupport, RepositoryBase):

    _dao_class = ArtistRecord

    _mapper = ArtistMapper()

    def find_by_user_id(self, user_id):
        condition = (UserCheckedArtistRecord.user_id == user_id,)
        return map(self._mapper.data2model,
                   ArtistRecord.query.join(UserCheckedArtistRecord).filter(*condition).all())

    def find_by_freebase_topic_id(self, freebase_topic_id):
        data = ArtistRecord.query.filter(ArtistRecord.freebase_topic_id == freebase_topic_id).first()
        if not data:
            return None
        else:
            return self._mapper.data2model(data)
