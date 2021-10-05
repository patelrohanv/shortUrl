from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.orm import mapper
from database import metadata, db_session


class ShortURL(object):
    query = db_session.query_property()

    id = Column(Integer, primary_key=True)
    url = Column(String(80), unique=True, nullable=False)
    short_link = Column(String, nullable=False)
    expiration_date = Column(DateTime, nullable=True)
    usage_count = Column(Integer, nullable=False, default=0)
    last_used = Column(DateTime, nullable=True)

    def __init__(self, url, short_link, expiration_date=None):
        self.url = url
        self.short_link = short_link
        self.expiration_date = expiration_date

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "short_link": self.short_link,
            "expiration_date": self.expiration_date,
            "usage_count": self.usage_count,
            "last_used": self.last_used
        }

    @staticmethod
    def serialize_list(urls_data):
        serialized = []
        for ud in urls_data:
            formatted = ud.serialize()
            serialized.append(formatted)
        return serialized

    def __repr__(self):
        return \
            f'<ShortURL \
            {self.id} {self.url} {self.short_link} {self.expiration_date} {self.usage_count} {self.last_used}>'


short_urls = Table('short_urls', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('url', String(80), unique=True, nullable=False),
                   Column('short_link', String, nullable=False),
                   Column('expiration_date', DateTime, nullable=True),
                   Column('usage_count', Integer, nullable=False, default=0),
                   Column('last_used', DateTime, nullable=True)
                   )
mapper(ShortURL, short_urls)
