# -*- coding: utf-8 -*-
from redis import StrictRedis
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def commit_with_fallback(session):
    """do commit. if exception occur, do rollback.

    :param session: session object
    :raise: Exception
    """
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise


db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
Base = declarative_base()

redis_session = StrictRedis()
