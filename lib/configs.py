from platformdirs import user_config_dir
from lib.logger import logger
import traceback
import json
import os

APP_NAME = "aurbit"
SERVER_CONFIG_FILE = "aurbit-server.json"
DEFAULT_CONFIG = {
    "PORT": 2872 # ( spells out the word aura on a keypad )
}

config_dir = user_config_dir(APP_NAME)
os.makedirs(config_dir, exist_ok=True)

def verify_config(data, data_type=dict, required=[]):
    if type(data) != data_type: return False

    for option in required:
        if option not in data:
            return False
        
    return True

def fetch_server_config():
    config_path = os.path.join(config_dir, SERVER_CONFIG_FILE)
    config = {} # -- default
    try:
        config = json.load(open(config_path, "r"))
    except Exception as e:
        # json syntax error
        logger.error(f"Unable to fetch required fields from config: {config_path} {traceback.format_exc()}")

    if not verify_config(config, dict, ["PORT"]):
        logger.warning(f"Unable to fetch config file: {config_path}")
        return DEFAULT_CONFIG

    return config