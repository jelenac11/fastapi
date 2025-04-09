import pytest


@pytest.mark.integration()
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Service is healthy!"}