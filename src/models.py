from src import db


class ShortURL(db.Model):
    __tablename__ = 'short_url'

    id = db.Column(db.Integer, primary_key=True)
    URL = db.Column(db.String(80), unique=True, nullable=False)
    shortLink = db.Column(db.String, nullable=False)
    expirationDate = db.Column(db.DateTime, nullable=True)
    usageCount = db.Column(db.Integer, nullable=False, default=0)
    lastUsed = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<ShortURL %r %r %r %r %r>' % \
               self.id, \
               self.URL, \
               self.shortLink, \
               self.expirationDate, \
               self.usageCount
