from datetime import datetime

class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    URL = db.Column(db.String(80), nullable=False)
    shortLink = db.Column(db.String, nullable=False)
    expirationDate = db.Column(db.DateTime, nullable=True)
    usageCount = db.Column(db.Integer)

    def __repr__(self):
        return '<ShortURL %r>' % self.URL
