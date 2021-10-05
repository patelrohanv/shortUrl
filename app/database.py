from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

from config import PostgresConfig

pgc = PostgresConfig()
engine = create_engine(
    f'postgresql://{pgc.getUser()}:{pgc.getPass()}@{pgc.getHost()}:{pgc.getPort()}/{pgc.getDb()}'

)

metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def init_db():
    metadata.create_all(bind=engine)
