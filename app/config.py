import os


class FlaskConfig:
    config = {
        'FLASK_HOST': os.getenv('FLASK_HOST'),
        'FLASK_PORT': os.getenv('FLASK_PORT'),
        'FLASK_APP': os.getenv('FLASK_APP'),
        'FLASK_ENV': os.getenv('FLASK_ENV'),
    }

    def __init__(self):
        self._config = self.config

    def getHost(self):
        return self._config['FLASK_HOST']

    def getPort(self):
        return self._config['FLASK_PORT']


class PostgresConfig:
    config = {
        'POSTGRES_USER': os.getenv('POSTGRES_USER'),
        'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'POSTGRES_HOST': os.getenv('POSTGRES_HOST'),
        'POSTGRES_PORT': os.getenv('POSTGRES_PORT'),
        'POSTGRES_DB': os.getenv('POSTGRES_DB')
    }

    def __init__(self):
        self._config = self.config

    def getUser(self):
        return self._config['POSTGRES_USER']

    def getPass(self):
        return self._config['POSTGRES_PASSWORD']

    def getHost(self):
        return self._config['POSTGRES_HOST']

    def getPort(self):
        return self._config['POSTGRES_PORT']

    def getDb(self):
        return self._config['POSTGRES_DB']
