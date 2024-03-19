from logging_config import production_logging_config, clear_file_handlers
from logging.config import dictConfig
import os

# Call this function to clear any existing file handlers
clear_file_handlers()

# Apply the production logging configuration
dictConfig(production_logging_config)

class ProductionConfig:
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///./mediqbackend.db")
    SQLALCHEMY_ECHO = False
    DEBUG = False
    # Any other production-specific configurations