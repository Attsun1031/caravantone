# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from caravantone import app


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


engine = create_engine(app.config['DB_URI'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base(bind=engine)
Base.query = db_session.query_property()
