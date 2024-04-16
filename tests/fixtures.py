import pytest
from app import create_app

@pytest.fixture
def get_url(api_url_prefix=False):
    """
    Is returned localhost url. Default 'http://127.0.0.1/'.

    : parameter api_url_prefix : bool

    If set, was returs url with api prefix 'http://127.0.0.1/api/v0.1'
    """
    BASE_URL_TEST = 'http://127.0.0.1/'
    API_PREFIX = 'api/v0.1'
    return BASE_URL_TEST + API_PREFIX if api_url_prefix else BASE_URL_TEST


@pytest.fixture
def app():
    app = create_app('dev')
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()