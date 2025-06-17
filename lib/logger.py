from platformdirs import user_config_dir
import logging
import os

APP_NAME = "aurbit"
HANDLERS = [
    ("error", logging.ERROR), 
    ("info", logging.INFO), 
    ("warning", logging.WARNING)]

config_dir = user_config_dir(APP_NAME)
os.makedirs(config_dir, exist_ok=True)

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)

logging_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

class LogLevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

for handler_name, handler_type in HANDLERS:
    handler = logging.FileHandler(os.path.join(config_dir, f"{handler_name}.log"))
    handler.setLevel(handler_type)
    handler.setFormatter(logging_format)
    handler.addFilter(LogLevelFilter(handler_type))
    logger.addHandler(handler)