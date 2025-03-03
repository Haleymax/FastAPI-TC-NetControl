import os
from configparser import ConfigParser

import yaml

from app.utils.logger import logger
from testing.core.all_path import config_path


def get_data_by_yaml(yaml_file_path):
    try:
        logger.info(f"load {os.path.basename(yaml_file_path)} ......")
        with open(yaml_file_path, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"load file happen error {e}")
        return None
    return data

def get_data_by_properties(properties_file_path):
    try:
        logger.info(f"load {os.path.basename(properties_file_path)} ......")
        config = ConfigParser(defaults=None)
        config.read(properties_file_path, encoding='utf-8')
        data = dict(config._sections)
    except Exception as e:
        logger.error(f"load file happen error {e}")
        return None
    return data


def get_config(config_file_path):
    yaml_data = get_data_by_yaml(config_file_path)
    return yaml_data


app_config = get_config(config_path)
print(app_config)