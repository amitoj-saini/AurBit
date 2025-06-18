from lib.initial import APP_NAME, CONFIG_DIR
import logging
import os

HANDLERS = [
    ("error", logging.ERROR), 
    ("info", logging.INFO), 
    ("warning", logging.WARNING)
]

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)

logging_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

class LogLevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

for handler_name, handler_type in HANDLERS:
    handler = logging.FileHandler(os.path.join(CONFIG_DIR, f"{handler_name}.log"))
    handler.setLevel(handler_type)
    handler.setFormatter(logging_format)
    handler.addFilter(LogLevelFilter(handler_type))
    logger.addHandler(handler)