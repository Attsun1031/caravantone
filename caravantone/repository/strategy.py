# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta


class RepositoryStrategyBase(metaclass=ABCMeta):

    @abstractmethod
    def find_by_id(self, ident):
        pass

    @abstractmethod
    def save(self, model, flush=True):
        pass


class DBStrategy(RepositoryStrategyBase):

    def __init__(self, dao_class, mapper, session=None):
        self.__dao_class = dao_class
        self.__mapper = mapper
        if session is None:
            from caravantone.dao import db_session
            self.__session = db_session
        else:
            self.__session = session

    def find_by_id(self, ident):
        data = self.__dao_class.query.get(ident)
        if data is not None:
            return self.__mapper.data2model(data)
        else:
            return data

    def save(self, model, flush=True):
        self.__session.add(self.__mapper.model2data(model))
        if flush:
            try:
                self.__session.commit()
            finally:
                self.__session.rollback()
