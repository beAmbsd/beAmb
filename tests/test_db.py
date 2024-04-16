from urllib.request import urlopen
import pytest
from app.models import User
from app.core import get_virt_env




def test_set_virt_env():
    """
    Is the environment variables set.
    """
    assert get_virt_env() == "environment is set"


def test_request_example(client):
    with urlopen(get_url()) as resp:
        html = resp.read()
        assert 'hello world' in html.lower()