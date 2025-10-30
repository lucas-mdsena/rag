from typing import Any, Dict

import yaml

from utils.setup_logger import logger



def read_yaml_file(yaml_file_path: str) -> Dict[str, Any]:
    """Reads a YAML file and returns it's content as a dictionary.

    :param yaml_file_path: path to yaml file.
    :return: YAML file content.
    """
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            logger.error(f"Error reading YAML file '{yaml_file_path}': {e}")
            return dict()
        except FileNotFoundError:
            logger.error(f"FILE {yaml_file_path} DOESN'T EXISTS")
            return dict()

settings = read_yaml_file("settings/config.yaml")