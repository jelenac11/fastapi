import pytest
from fastapi.testclient import TestClient
import sys

sys.path.append("./src")
from main import app

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c