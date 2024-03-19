# test_logging.py

import logging
import logging.config
import logging_config  # This imports your logging configurations

logging_config.clear_file_handlers()

logging.config.dictConfig(logging_config.development_logging_config)
# logging.config.dictConfig(logging_config.production_logging_config)
# logging.config.dictConfig(logging_config.testing_logging_config)

# Get the logger
logger = logging.getLogger(__name__)

# Log messages at different levels
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")

print("Logging test completed. Please check the console output and the log files.")