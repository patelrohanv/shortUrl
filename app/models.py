from app import db


class ShortURL(db.Model):
    __tablename__ = 'short_url'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80), unique=True, nullable=False)
    short_link = db.Column(db.String, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=True)
    usage_count = db.Column(db.Integer, nullable=False, default=0)
    last_used = db.Column(db.DateTime, nullable=True)

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
    def serialize_list(short_urls):
        serialized = []
        for ud in short_urls:
            formatted = ud.serialize()
            serialized.append(formatted)
        return serialized

    def __repr__(self):
        return \
            f'<ShortURL \
            {self.id} {self.url} {self.short_link} {self.expiration_date} {self.usage_count} {self.last_used}>'
