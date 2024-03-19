# logging_config.py

import os
import logging
import copy  # Import the copy module for deep copying


suppress_libs = ['httpcore', 'httpx', 'requests', 'urllib3', 'openai']
# Set the logging level for each library to CRITICAL
for lib in suppress_libs:
    logging.getLogger(lib).setLevel(logging.CRITICAL)

class RelativePathFormatter(logging.Formatter):
    def format(self, record):
        # Get the absolute path of the log record
        absolute_path = record.pathname
        # Check if the absolute path and the __file__ are on the same drive
        if os.path.splitdrive(absolute_path)[0] == os.path.splitdrive(__file__)[0]:
            # Convert it to a relative path if on the same drive
            relative_path = os.path.relpath(absolute_path, start=os.path.dirname(__file__))
            # Update the record's pathname to the relative path
            record.pathname = relative_path
        else:
            # If on different drives, just use the absolute path
            record.pathname = absolute_path
        # Now format the record as usual
        return super(RelativePathFormatter, self).format(record)
    
# Define common log file paths (you can change these to match your environment)
development_log_file = os.path.join('logs', 'development.log')
production_log_file = os.path.join('logs', 'production.log')
testing_log_file = os.path.join('logs', 'testing.log')

# Ensure the 'logs' directory exists
os.makedirs('logs', exist_ok=True)

# Base logging configuration
base_logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            '()': RelativePathFormatter,
            'format': '%(asctime)s - %(name)s:%(lineno)d:%(levelname)s = %(message)s - %(pathname)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',  # Use standard output
        },
        # 'file' handler will be added per environment
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console'],  # file handler will be added per environment
            'level': 'WARNING',
        },
    },
}

# Update the 'file' handler for each specific configuration
def configure_file_handler(config, filename):
    file_handler = {
        'class': 'logging.FileHandler',
        'formatter': 'simple',
        'filename': filename,
        'mode': 'a',
        'level': 'DEBUG',  # Set the level for the file handler if necessary
    }
    config['handlers']['file'] = file_handler
    config['loggers']['']['handlers'].append('file')

# Create the specific logging configurations using a deep copy
development_logging_config = copy.deepcopy(base_logging_config)
configure_file_handler(development_logging_config, development_log_file)
development_logging_config['loggers']['']['level'] = 'DEBUG'

production_logging_config = copy.deepcopy(base_logging_config)
configure_file_handler(production_logging_config, production_log_file)
production_logging_config['loggers']['']['level'] = 'INFO'

testing_logging_config = copy.deepcopy(base_logging_config)
configure_file_handler(testing_logging_config, testing_log_file)
testing_logging_config['loggers']['']['level'] = 'CRITICAL'

# Function to clear existing file handlers (to be called before dictConfig)
def clear_file_handlers():
    root_logger = logging.getLogger()
    handlers = root_logger.handlers[:]
    for handler in handlers:
        if isinstance(handler, logging.FileHandler):
            root_logger.removeHandler(handler)
            handler.close()