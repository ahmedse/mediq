from logging_config import testing_logging_config, clear_file_handlers
from logging.config import dictConfig
import os

# Call this function to clear any existing file handlers
clear_file_handlers()

# Apply the testing logging configuration
dictConfig(testing_logging_config)

class TestingConfig:
    DATABASE_URI = "sqlite:///./test_mediqbackend.db"  # Example SQLite database
    SQLALCHEMY_ECHO = True
    TESTING = True
    # Any other testing-specific configurations