from flask import Flask, request, jsonify

app = Flask(__name__)



@app.route("/ping")
def ping():
    return "<p>Ping!</p>"


@app.route('/findLong', methods=['GET'])
def findLong():
    shortLink = request.args.get('shortLink')
    return jsonify(shortLink)


@app.route('/findLong', methods=['GET'])
def findLong():
    fullUrl = request.args.get('fullUrl')
    return jsonify(fullUrl)
