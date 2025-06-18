from platformdirs import user_config_dir
import os

APP_NAME = "aurbit"
CONFIG_DIR = user_config_dir(APP_NAME)


def setup():
    os.makedirs(CONFIG_DIR, exist_ok=True)