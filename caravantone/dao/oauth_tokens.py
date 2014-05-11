# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from caravantone.dao.base import Base
from caravantone.dao.users import UserRecord


class OauthTokenRecord(Base):

    __tablename__ = 'oauth_tokens'
    __table_args__ = {'mysql_engine': 'innoDB'}

    user_id = Column(INTEGER(unsigned=True), ForeignKey(UserRecord.id), primary_key=True)
    provider_type = Column(TINYINT(unsigned=True), primary_key=True, autoincrement=False)
    access_token = Column(String(255), nullable=False)
    access_secret = Column(String(255), nullable=False)
