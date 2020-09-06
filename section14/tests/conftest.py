import pytest


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv('FROM_EMAIL', 'some@email.com')
    # monkeypatch.setenv('ANOTHER_SETTING', 'some-value')