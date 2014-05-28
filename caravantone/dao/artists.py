# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.mysql import INTEGER
from caravantone.dao.base import Base


class ArtistRecord(Base):

    __tablename__ = 'artists'
    __table_args__ = {'mysql_engine': 'innoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True)
    name = Column(String(255), nullable=False)
    freebase_topic_id = Column(String(100), nullable=True)
    registered_datetime = Column(DateTime, default=datetime.datetime.now)
    updated_datetime = Column(DateTime, onupdate=datetime.datetime.now)
