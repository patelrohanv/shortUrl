import pytest
from unittest import mock
import os

import app.routes as routes


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {'FLASK_HOST': '127.0.0.1', 'FLASK_PORT': '5000'}):
        yield


class TestRoutes:
    def testhasActiveAccount(self):
        result = routes.ping()
        expected = "<p>Ping!</p>"
        assert(result, expected)
