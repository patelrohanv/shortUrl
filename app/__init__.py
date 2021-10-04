from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import FlaskConfig, PostgresConfig

app = Flask(__name__)

fc = FlaskConfig()
pgc = PostgresConfig()

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{pgc.getUser()}:{pgc.getPass()}@{pgc.getHost()}:{pgc.getPort()}/{pgc.getDb()}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()


@app.before_first_request
def initialize_database():
    db.create_all()


if __name__ == "__main__":
    host = fc.getHost()
    port = fc.getPort()
    app.run(app.run(host=host, port=int(port)))
