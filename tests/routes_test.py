from app.routes import short
from flask import Flask

app = Flask(__name__)


app.register_blueprint(short, url_prefix='')


class TestRoutes:
    def testPing(self):
        result = app.routes.ping()
        expected = "<p>Ping!</p>"
        assert (result, expected)
