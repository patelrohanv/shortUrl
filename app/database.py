from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import PostgresConfig

pgc = PostgresConfig()
engine = create_engine(
    f'postgresql://{pgc.getUser()}:{pgc.getPass()}@{pgc.getHost()}:{pgc.getPort()}/{pgc.getDb()}'

)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
