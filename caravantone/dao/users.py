# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from caravantone.dao.base import Base


class User(Base):

    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'innoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True)
    name =Column(String(255), nullable=False)
    profile = Column(Text, nullable=True)
