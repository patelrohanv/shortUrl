from database import db_session
from models import ShortURL

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, NoResultFound
from datetime import datetime
import shortuuid


short = Blueprint("short", __name__)
db = db_session()


@short.route("/ping")
def ping():
    return "<p>Ping!</p>"


@short.route('/generateShortLink', methods=['POST'])
def generate_short_link():
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

    if 'expiration_date' in data:
        try:
            expiration_date = datetime.strptime(data['expiration_date'], "%m/%d/%Y")
        except ValueError as ve:
            return jsonify(str(ve)), 400
    else:
        expiration_date = None

    short_link = shortuuid.uuid()

    try:
        entry = ShortURL(
            url=url,
            short_link=short_link,
            expiration_date=expiration_date
        )
        db.add(entry)
        db.commit()
        ret = entry.serialize()
        return jsonify(ret), 200
    except IntegrityError as ie:
        return jsonify(f'Key {url} already exists'), 400


@short.route('/<short_link>', methods=['GET'])
def find_url_from_short_link(short_link):
    """Find a shortlink for a url

    Parameters
    ----------
    short_link: `string`
        The shortLink whose URL to find

    Returns
    -------
    url: `string`
        The Found url for the provided shortLink.
        Returns "NOT FOUND" if the provided url  does not exist
        Returns "SHORTLINK EXPIRED" if the provided url does not exist
    """
    entry = ShortURL.query.filter_by(short_link=short_link).one()
    # Send 400 if shortLink is not found
    if not entry:
        return jsonify('shortLink not found'), 400

    if entry.expiration_date is not None:
        if entry.expiration_date < datetime.now():
            db.delete(entry)
            db.commit()
            return jsonify('shortLink expired; please recreate'), 400

    # Update the usageCount and lastUsed
    entry.usage_count += 1;
    entry.last_used = datetime.now()
    db.add(entry)
    db.commit()
    ret = entry.serialize()
    return jsonify(ret), 200


@short.route('/delete/url', methods=['DELETE'])
def delete_url():
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
        entry = ShortURL.query.filter_by(url=url).one()
        db.delete(entry)
        db.commit()
        return jsonify("Delete Successful"), 200
    except NoResultFound:
        return jsonify("url not found"), 400


@short.route('/delete/shortLink', methods=['DELETE'])
def delete_short_link():
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
    if 'short_link' not in data:
        return jsonify('Missing required field \'shortLink\' in request body'), 400
    short_link = data['short_link']

    try:
        entry = ShortURL.query.filter_by(short_link=short_link).one()
        db.delete(entry)
        db.commit()
        return jsonify("Delete Successful"), 200
    except NoResultFound:
        return jsonify("shortLink not found"), 400


@short.route('/delete/expired', methods=['DELETE'])
def delete_expired():
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
        if entry.expiration_date is None:
            continue
        if entry.expiration_date <= datetime.now():
            db.delete(entry)
            db.commit()
    return jsonify("Delete Successful"), 200


@short.route('/analytics/', methods=['GET'])
def get_all():
    """Get a list of URLs and their usage count in descending order

    Parameters
    ----------

    Returns
    -------
    result: `string`
        The result of deleting the shortlink. Returns "NOT FOUND" if the provided shortlink does not exist
    """
    select_all = ShortURL.query.all()
    ret = ShortURL.serialize_list(select_all)
    return jsonify(ret), 200


@short.route('/analytics/popular', methods=['GET'])
def get_popular():
    """Get a list of URLs and their usage count in descending order

    Parameters
    ----------

    Returns
    -------
    result: `string`
        The result of deleting the shortlink. Returns "NOT FOUND" if the provided shortlink does not exist
    """
    data = ShortURL.query.order_by(ShortURL.usage_count.desc()).all()
    ret = []
    for d in data:
        ret.append({"url": d.url, "short_link": d.short_link, "usage_count": d.usage_count})
    return jsonify(ret), 200


@short.route('/analytics/recent', methods=['GET'])
def get_recent():
    """Get a list of URLs and their usage count, and last clicked date

    Parameters
    ----------

    Returns
    -------
    result: `string`
        The result of deleting the shortlink. Returns "NOT FOUND" if the provided shortlink does not exist
    """
    data = ShortURL.query.order_by(ShortURL.last_used.desc()).all()
    ret = []
    for d in data:
        ret.append({"url": d.url, "short_link": d.short_link, "last_used": d.last_used})
    return jsonify(ret), 200

