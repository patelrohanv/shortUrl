from app import db


class ShortURL(db.Model):
    __tablename__ = 'short_url'

    id = db.Column(db.Integer, primary_key=True)
    URL = db.Column(db.String(80), unique=True, nullable=False)
    shortLink = db.Column(db.String, nullable=False)
    expirationDate = db.Column(db.DateTime, nullable=True)
    usageCount = db.Column(db.Integer, nullable=False, default=0)
    lastUsed = db.Column(db.DateTime, nullable=True)

    def __init__(self, URL, shortLink, expirationDate=None):
        self.URL = URL
        self.shortLink = shortLink
        self.expirationDate = expirationDate

    def serialize(self):
        return {
            "id": self.id,
            "url": self.URL,
            "shortLink": self.shortLink,
            "expirationDate": self.expirationDate,
            "usageCount": self.usageCount,
            "lastUsed": self.lastUsed
        }

    @staticmethod
    def serializeList(shorturls):
        serialized = []
        for ud in shorturls:
            formatted = ud.serialize()
            serialized.append(formatted)
        return serialized

    def __repr__(self):
        return f'<ShortURL {self.id} {self.URL} {self.shortLink} {self.expirationDate} {self.usageCount}>'
