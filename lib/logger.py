from lib.initial import APP_NAME, CONFIG_DIR
import logging
import os

def new_logger(level, name):
    logging.addLevelName(level, name)
    
    def child_logger(self, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)
    
    setattr(logging.Logger, name.lower(), child_logger)

HANDLERS = [
    ("error", logging.ERROR),
    ("info", logging.INFO),
    ("warning", logging.WARNING),
    ("access", 16),
    ("http", 15)
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
    if not hasattr(logging.Logger, handler_name):
        new_logger(handler_type, handler_name)
    handler = logging.FileHandler(os.path.join(CONFIG_DIR, f"{handler_name}.log"))
    handler.setLevel(handler_type)
    handler.setFormatter(logging_format)
    handler.addFilter(LogLevelFilter(handler_type))
    logger.addHandler(handler)