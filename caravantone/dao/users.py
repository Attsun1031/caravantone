# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text
from caravantone.dao.base import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name =Column(String(255))
    profile = Column(Text)


if __name__ == '__main__':
    print(Base.metadata.create_all())
