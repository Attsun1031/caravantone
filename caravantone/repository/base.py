# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta


class Repository(metaclass=ABCMeta):

    @abstractmethod
    def find_by_id(self, ident):
        pass

    @abstractmethod
    def save(self, model, flush=True):
        pass


class MapperBase(metaclass=ABCMeta):
    @abstractmethod
    def data2model(self, data):
        pass

    @abstractmethod
    def model2data(self, model):
        pass
