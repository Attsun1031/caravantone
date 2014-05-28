# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import INTEGER
from caravantone.dao.base import Base


class UserCheckedArtistRecord(Base):

    __tablename__ = 'user_checked_artists'
    __table_args__ = {'mysql_engine': 'innoDB'}

    user_id = Column(INTEGER(unsigned=True), ForeignKey('users.id'), primary_key=True)
    artist_id = Column(INTEGER(unsigned=True), ForeignKey('artists.id'), primary_key=True)
    registered_datetime = Column(DateTime, default=datetime.datetime.now)
