from flask import Flask
from config import FlaskConfig
from routes import short

from database import init_db, db_session

app = Flask(__name__)
init_db()
app.register_blueprint(short)

fc = FlaskConfig()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    host = fc.getHost()
    port = fc.getPort()
    app.run(host="0.0.0.0", port=int(port))
