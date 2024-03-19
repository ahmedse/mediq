# test_services.py
import pytest
from fastapi import HTTPException
from unittest.mock import patch, Mock
from app.models import ServiceType
from app.services import TextProcessingService

# Constants for tests
VALID_TEXT = "This is a valid text for processing."
INVALID_TEXT = "A"
VALID_SERVICE_TYPE = ServiceType.TRANSLATION.name
INVALID_SERVICE_TYPE = "INVALID_SERVICE_TYPE"

@pytest.fixture
def service_instance():
    """Fixture to create a new TextProcessingService instance for each test."""
    return TextProcessingService(
        service_type=VALID_SERVICE_TYPE,
        text=VALID_TEXT,
        academic_year="2023",
        course_code="MED101",
        course_title="Introduction to Medicine",
        lecture_title="The Human Anatomy",
        topic="Cardiology",
        user_prompt="Please explain the concept of cardiac output."
    )

@pytest.fixture
def service_instance_with_invalid_type():
    """Fixture to create a new TextProcessingService instance with an invalid service type."""
    return TextProcessingService(
        service_type=INVALID_SERVICE_TYPE,
        text=VALID_TEXT
    )

@pytest.fixture
def service_instance_with_invalid_text():
    """Fixture to create a new TextProcessingService instance with invalid text."""
    return TextProcessingService(
        service_type=VALID_SERVICE_TYPE,
        text=INVALID_TEXT
    )

def test_process_text_with_valid_data(service_instance):
    with patch('app.services.crud') as mock_crud, \
         patch('app.services.SessionLocal') as mock_session:
        # Mock the session and the crud operations
        mock_session.return_value = Mock()
        mock_crud.create_service_request.return_value = Mock()
        
        # Mock the OpenAI response
        with patch('app.services.OpenAI') as mock_openai:
            mock_openai.return_value.chat.completions.create.return_value = Mock(
                choices=[Mock(message=Mock(content="Translated text"))]
            )
            
            # Call the process_text method
            result = service_instance.process_text()
            
            # Assertions to ensure the process_text method is functioning as expected
            assert result['context_prompt'] is not None
            assert result['user_response'] is not None
            assert result['processing_time'] is not None
            assert 'Translated text' in result['user_response']
            mock_crud.create_service_request.assert_called_once()
            mock_openai.return_value.chat.completions.create.assert_called_once()

def test_process_text_with_invalid_service_type(service_instance_with_invalid_type):
    # Expect an HTTPException when an invalid service type is used
    with pytest.raises(HTTPException) as exc_info:
        service_instance_with_invalid_type.process_text()
    assert exc_info.value.status_code == 400
    assert "Invalid service type" in str(exc_info.value.detail)

def test_process_text_with_invalid_text(service_instance_with_invalid_text):
    # Expect an HTTPException when invalid text is used
    with pytest.raises(HTTPException) as exc_info:
        service_instance_with_invalid_text.process_text()
    assert exc_info.value.status_code == 400
    assert "Text must not be empty and must have at least 2 characters" in str(exc_info.value.detail)

# Add more tests for other methods like _handle_translation and construct_prompt_inputs