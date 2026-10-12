import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client():
    application = create_app("sqlite://", seed=False)
    with TestClient(application) as test_client:
        yield test_client
