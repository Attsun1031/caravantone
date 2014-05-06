# -*- coding: utf-8 -*-
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from caravantone.dao.base import Base


class Artist(Base):

    __tablename__ = 'artists'
    __table_args__ = {'mysql_engine': 'innoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True)
    name =Column(String(255), nullable=False)
    freebase_topic_id =Column(String(100), nullable=True)
