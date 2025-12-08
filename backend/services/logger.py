import logging
import sys
import os
from config.settings import LOG_LEVEL, LOG_FILE

# Create logs directory
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configure logger
logger = logging.getLogger("QuranSearch")
logger.setLevel(getattr(logging, LOG_LEVEL))

# Handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, LOG_LEVEL))

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(getattr(logging, LOG_LEVEL))

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.propagate = False

logger.info("Logger initialized")