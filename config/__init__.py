# config/__init__.py
import os
from dotenv import load_dotenv
load_dotenv(override=True) 
from .testing import TestingConfig
from .development import DevelopmentConfig
from .production import ProductionConfig
import logging.config
from logging_config import clear_file_handlers, testing_logging_config, development_logging_config, production_logging_config

# development, production, testing
environment = os.getenv('ENVIRONMENT', 'development')
# environment = 'production'

# Clear any existing file handlers before applying new configuration
clear_file_handlers()

# Select the appropriate configuration class based on the environment variable
if environment == 'testing':
    AppConfig = TestingConfig
    logging.config.dictConfig(testing_logging_config)
elif environment == 'production':
    AppConfig = ProductionConfig
    logging.config.dictConfig(production_logging_config)
else:
    AppConfig = DevelopmentConfig
    logging.config.dictConfig(development_logging_config)
logger = logging.getLogger(__name__)
