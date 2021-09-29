from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import shortuuid

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
# db = SQLAlchemy(app)
db = {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


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
    expiration = request.args.get('expiration')
    link = f'http://0.0.0.0:5000/{shortuuid.uuid()}'
    db[url] = link
    return jsonify(link)


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
    url = next(key for key, value in db.items() if value == shortLink)
    return jsonify(url)


@app.route('/deleteShortLink', methods=['DELETE'])
def deleteShortLink():
    """Delete a shortlink

    Parameters
    ----------
    shortLink: `string`
        The shortlink whose entry to delete

    Returns
    -------
    result: `string`
        The result of deleting the shortlink. Returns "NOT FOUND" if the provided shortlink does not exist
    """
    url = request.args.get('url')
    del db[url]
    return jsonify(True)


@app.route('/deleteURL', methods=['DELETE'])
def deleteURL():
    """Delete a URL

    Parameters
    ----------
    URL: `string`
        The URL whose entry to delete

    Returns
    -------
    result: `string`
        The result of deleting the shortlink. Returns "NOT FOUND" if the provided shortlink does not exist
    """
    shortLink = request.args.get('shortLink')
    url = next(key for key, value in db.items() if value == shortLink)
    del db[url]
    return jsonify(True)


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