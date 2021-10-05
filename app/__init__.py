from flask import Flask

from config import FlaskConfig
from routes import short
from database import init_db, db_session


def create_app():
    app = Flask(__name__)
    init_db()
    app.register_blueprint(short)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


if __name__ == "__main__":
    fc = FlaskConfig()
    host = fc.getHost()
    port = fc.getPort()
    app = create_app()
    app.run(host=host, port=int(port))


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
