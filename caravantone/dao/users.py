# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text
from caravantone.dao.base import Base


class User(Base):

    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'innoDB'}

    id = Column(Integer, primary_key=True)
    name =Column(String(255), nullable=False)
    profile = Column(Text, nullable=False)
