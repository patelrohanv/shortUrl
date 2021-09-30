from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import shortuuid
import os

FLASK_HOST = os.getenv('FLASK_HOST')
FLASK_PORT = os.getenv('FLASK_PORT')

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    URL = db.Column(db.String(80), unique=True, nullable=False)
    shortLink = db.Column(db.String, nullable=False)
    expirationDate = db.Column(db.DateTime, nullable=True)
    usageCount = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<ShortURL %r>' % self.URL


if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT)
    db.create_all()


@app.route("/ping")
def ping():
    return "<p>Ping!</p>"


@app.route('/generateShortLink', methods=['POST'])
def generateShortLink():
    """Generate a shortlink for a url

    Parameters
    ----------
    url: `string`
        The Url to be shortlinked
    expiration: `string`, optional
        How long the generated shortlink should persist before being deleted

    Returns
    -------
    link: `string`
        The generated shortlink for the provided url
    """
    url = request.args.get('url')
    expiration = request.args.get('expiration') if request.args.get('expiration') else None
    link = shortuuid.uuid()
    entry = ShortURL(
        URL=url,
        link=link,
        expiration=expiration
    )
    db.session.add(entry)
    db.session.commit()
    print(entry)
    return jsonify(entry)


@app.route('/<shortLink>}', methods=['GET'])
def findURL(shortLink):
    """Find a shortlink for a url

    Parameters
    ----------
    shortLink: `string`
        The shortLink whose URL to find

    Returns
    -------
    url: `string`
        The Found url for the provided shortLink.
        Returns "NOT FOUND" if the provided url  does not exist
        Returns "SHORTLINK EXPIRED" if the provided url does not exist
    """
    entry = ShortURL.query.filter_by(shortLink=shortLink).first()
    print(entry)
    return jsonify(entry.URL)


@app.route('/deleteURL', methods=['DELETE'])
def deleteURL():
    """Delete a URL

    Parameters
    ----------
    url: `string`
        The URL whose entry to delete

    Returns
    -------
    result: `string`
        The result of deleting the shortlink. Returns "NOT FOUND" if the provided shortlink does not exist
    """
    url = request.args.get('url')
    entry = ShortURL(URL=url)
    db.session.delete(entry)
    db.session.commit()
    print(entry)
    return jsonify(entry)


@app.route('/analytics', methods=['GET'])
def getAnalytics():
    """Get a list of URLs and their usage count in descending order

    Parameters
    ----------

    Returns
    -------
    result: `string`
        The result of deleting the shortlink. Returns "NOT FOUND" if the provided shortlink does not exist
    """
    return True


@app.route('/usage', methods=['GET'])
def getUsage():
    """Get a list of URLs and their usage count, and last clicked date

    Parameters
    ----------

    Returns
    -------
    result: `string`
        The result of deleting the shortlink. Returns "NOT FOUND" if the provided shortlink does not exist
    """
    return True
