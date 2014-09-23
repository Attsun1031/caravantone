# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER
from caravantone.dao.base import Base
from caravantone.dao.user_checked_artists import UserCheckedArtistRecord


class UserRecord(Base):

    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'innoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True)
    name = Column(String(255), nullable=False)
    profile = Column(Text, nullable=True)
    password = Column(String(255), nullable=True)   # oauth認証があり得る

    checked_artists = relationship('ArtistRecord',
                                   secondary=UserCheckedArtistRecord.__table__,
                                   backref='users',
                                   innerjoin=True)

    oauth_tokens = relationship('OauthTokenRecord', backref='user')

    registered_datetime = Column(DateTime, default=datetime.datetime.now)
    updated_datetime = Column(DateTime, onupdate=datetime.datetime.now)
