from fastapi.testclient import TestClient
from app.main import app  # Adjust the import path based on your application structure
from app.schemas import TextProcessingTaskCreate, ServiceType  # Adjust the import path
from pytest import raises
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
import pytest

# Set up a fixture for the test client
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# Now define the test function
def test_process_text(client):
    test_data = {
        "text": "This is a test text",
        "service_type": "Translation"  # Make sure this matches one of the enums
    }

    # Send a POST request to the process_text endpoint
    response = client.post("/process_text/", json=test_data)

    # Assert that the status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response contains the expected keys
    response_data = response.json()
    assert "response" in response_data

    # If you know what the processed text should look like,
    # you can also assert the content of the response
    # For example, if you know the service just echoes the text for testing:
    expected_response = test_data["text"]
    assert response_data["response"] == expected_response

    # Add more assertions as necessary to fully test your endpoint's functionality

    # Test invalid input
def test_process_text_invalid_input(client):
    test_data = {
        "text": "",  # Empty text field
        "service_type": "Translation"
    }
    response = client.post("/process_text/", json=test_data)
    assert response.status_code == HTTP_400_BAD_REQUEST

# Test invalid service type
def test_process_text_invalid_service_type(client):
    test_data = {
        "text": "This is a test text",
        "service_type": "InvalidServiceType"
    }
    response = client.post("/process_text/", json=test_data)
    assert response.status_code == HTTP_400_BAD_REQUEST