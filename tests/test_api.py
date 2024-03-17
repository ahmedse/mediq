# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db(test_db):
    pass  # The fixture will run automatically before the tests because of `autouse=True`

def test_create_item():
    response = client.post("/items/", json={"name": "Test item", "description": "A test item", "price": 50})
    assert response.status_code == 200
    assert response.json()["name"] == "Test item"

# Add more tests for other endpoints...