from logging_config import development_logging_config, clear_file_handlers
from logging.config import dictConfig
import os

# Call this function to clear any existing file handlers
clear_file_handlers()

# Apply the development logging configuration
dictConfig(development_logging_config)

class DevelopmentConfig:
    DATABASE_URI = os.getenv("DEV_DATABASE_URI", "sqlite:///./dev_mediqbackend.db")  # Example SQLite database
    SQLALCHEMY_ECHO = True
    DEBUG = True
    # Any other development-specific configurations