from app import app, db
from app.models import ShortURL

from flask import request, jsonify
from sqlalchemy.exc import IntegrityError, NoResultFound
from datetime import datetime
import shortuuid
import os

FLASK_HOST = os.getenv('FLASK_HOST')
FLASK_PORT = os.getenv('FLASK_PORT')


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
    # Send 400 if url is not provided
    if 'url' not in data:
        return jsonify('Missing required field \'url\' in request body'), 400
    url = data['url']

    if 'expirationDate' in data:
        try:
            expirationDate = datetime.strptime(data['expirationDate'], "%m/%d/%Y")
        except ValueError as ve:
            app.logger.info(ve)
            return jsonify(str(ve)), 400
    else:
        expirationDate = None

    shortLink = shortuuid.uuid()

    try:
        entry = ShortURL(
            URL=url,
            shortLink=shortLink,
            expirationDate=expirationDate
        )
        db.session.add(entry)
        db.session.commit()
        ret = entry.serialize()
        return jsonify(ret), 200
    except IntegrityError as ie:
        app.logger.info(ie)
        return jsonify(f'Key {url} already exists'), 400


@app.route('/<shortLink>', methods=['GET'])
def findURLFromShortLink(shortLink):
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

    if entry.expirationDate is not None:
        if entry.expirationDate < datetime.now():
            db.session.delete(entry)
            db.session.commit()
            return jsonify('shortLink expired; please recreate'), 400

    # Update the usageCount and lastUsed
    entry.usageCount += 1;
    entry.lastUsed = datetime.now()
    db.session.add(entry)
    db.session.commit()
    ret = entry.serialize()
    return jsonify(ret), 200


@app.route('/delete/url', methods=['DELETE'])
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
    # Send 400 if url is not provided
    if 'url' not in data:
        return jsonify('Missing required field \'url\' in request body'), 400
    url = data['url']

    try:
        entry = ShortURL.query.filter_by(URL=url).one()
        db.session.delete(entry)
        db.session.commit()
        return jsonify("Delete Successful"), 200
    except NoResultFound as nrf:
        app.logger.info(nrf)
        return jsonify("url not found"), 400


@app.route('/delete/shortLink', methods=['DELETE'])
def deleteShortLink():
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
    # Send 400 if url is not provided
    if 'shortLink' not in data:
        return jsonify('Missing required field \'shortLink\' in request body'), 400
    shortLink = data['shortLink']

    try:
        entry = ShortURL.query.filter_by(shortLink=shortLink).one()
        db.session.delete(entry)
        db.session.commit()
        return jsonify("Delete Successful"), 200
    except NoResultFound as nrf:
        app.logger.info(nrf)
        return jsonify("shortLink not found"), 400


@app.route('/delete/expired', methods=['DELETE'])
def deleteExpired():
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

    # TODO find a cleaner way to do this without looping
    entries = ShortURL.query.all()
    for entry in entries:
        if entry.expirationDate is None:
            continue
        if entry.expirationDate <= datetime.now():
            db.session.delete(entry)
            db.session.commit()
    return jsonify("Delete Successful"), 200


@app.route('/analytics/', methods=['GET'])
def getAll():
    """Get a list of URLs and their usage count in descending order

    Parameters
    ----------

    Returns
    -------
    result: `string`
        The result of deleting the shortlink. Returns "NOT FOUND" if the provided shortlink does not exist
    """
    all = ShortURL.query.all()
    ret = ShortURL.serializeList(all)
    return jsonify(ret), 200


@app.route('/analytics/popular', methods=['GET'])
def getPopular():
    """Get a list of URLs and their usage count in descending order

    Parameters
    ----------

    Returns
    -------
    result: `string`
        The result of deleting the shortlink. Returns "NOT FOUND" if the provided shortlink does not exist
    """
    usageData = ShortURL.query.order_by(ShortURL.usageCount.desc()).all()
    ret = []
    for ud in usageData:
        ret.append({"url": ud.URL, "shortLink": ud.shortLink, "usageCount": ud.usageCount})
    return jsonify(ret), 200


@app.route('/analytics/recent', methods=['GET'])
def getRecent():
    """Get a list of URLs and their usage count, and last clicked date

    Parameters
    ----------

    Returns
    -------
    result: `string`
        The result of deleting the shortlink. Returns "NOT FOUND" if the provided shortlink does not exist
    """
    usageData = ShortURL.query.order_by(ShortURL.lastUsed.desc()).all()
    ret = []
    for ud in usageData:
        ret.append({"url": ud.URL, "shortLink": ud.shortLink, "lastUsed": ud.lastUsed})
    return jsonify(ret), 200

