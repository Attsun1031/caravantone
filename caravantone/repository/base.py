# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta
from caravantone.dao import db_session


class RepositoryBase(metaclass=ABCMeta):

    @abstractmethod
    def find_by_id(self, ident):
        pass

    @abstractmethod
    def save(self, model, flush=True):
        pass


class DBSupport(object):

    _dao_class = None

    _mapper = None

    session = db_session

    def find_by_id(self, ident):
        data = self._dao_class.query.get(ident)
        if data is not None:
            return self._mapper.data2model(data)
        else:
            return data

    def save(self, model, flush=True):
        data = self._mapper.model2data(model)
        self.session.add(data)
        if flush:
            try:
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise e
            else:
                # if committed, data would be modified (ex: auto incremented id)
                self._after_save(model, data)

    def _after_save(self, model, data):
        pass


class MapperBase(metaclass=ABCMeta):
    @abstractmethod
    def data2model(self, data):
        pass

    @abstractmethod
    def model2data(self, model):
        pass
