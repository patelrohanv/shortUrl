from src import app, db
from src.models import ShortURL

from flask import request, jsonify
import shortuuid

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
    response: `Response`
        The generated shortlink for the provided url
    """
    data = request.get_json()
    print(data)
    # Send 400 if url is not provided
    if 'url' not in data:
        return jsonify('Missing required field \'url\' in request body'), 400
    url = data['url']

    if 'expiration' in data:
        expirationDate = data['expiration']
    else:
        expirationDate = None

    shortLink = shortuuid.uuid()

    entry = ShortURL(
        URL=url,
        shortLink=shortLink,
        expirationDate=expirationDate
    )
    db.session.add(entry)
    db.session.commit()
    print(entry)
    return jsonify(entry), 201


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
    # Send 400 if shortLink is not found
    if not entry:
        return jsonify('shortLink not found'), 400

    # Update the usageCount
    entry.usageCount += 1;
    db.session.add(entry)
    db.session.commit()
    print(entry)
    return jsonify(entry.URL), 201


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
    data = request.get_json()
    print(data)
    # Send 400 if url is not provided
    if 'url' not in data:
        return jsonify('Missing required field \'url\' in request body'), 400
    url = data['url']

    entry = ShortURL.query.filter_by(URL=url).one()
    # Send 400 if shortLink is not found
    if not entry:
        return jsonify('shortLink not found for url'), 400

    db.session.delete(entry)
    db.session.commit()
    print(entry)
    return jsonify("Delete Successful"), 200


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
    usageData = ShortURL.query.order_by(ShortURL.usageCount).all()
    return jsonify(usageData), 200


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
