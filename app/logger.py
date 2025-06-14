# app/logger.py
import logging
import logging.handlers
import json
from pythonjsonlogger import jsonlogger
import os

# Path for logs folder outside the app directory, relative to app/logger.py location
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, 'app.log')

class JsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        # Add extra fields or customize if needed
        if not log_record.get('level'):
            log_record['level'] = record.levelname
        if not log_record.get('timestamp'):
            log_record['timestamp'] = self.formatTime(record, self.datefmt)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Log all levels DEBUG and above

    if not logger.hasHandlers():
        # File handler with rotation: 5 files max, 1MB each
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE_PATH, maxBytes=1_000_000, backupCount=5, encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)

        # JSON formatter for structured logs
        formatter = JsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        # Optional: also log to console (stdout)
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger

# Usage example (remove/comment out before production or tests)
# logger = get_logger(__name__)
# logger.info("Logger initialized")
