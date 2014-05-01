# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_config = 'mysql://root:@127.0.0.1/caravantone'
engine = create_engine(db_config, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base(bind=engine)


def init_db():
    import caravantone.dao
    print(Base.metadata.create_all(bind=engine))

init_db()

