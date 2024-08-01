import yaml
import logging
from typing import List, Literal
from ..errors import YamlParseError
import logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)
import re 
import os

class Settings(dict):
    """
    Represents app settings yaml file
    """

    def __init__(self, section: Literal['llm', 'embeddings', 'vectordb'], path='./app-settings.yaml', **kwargs):
        """
        Reads given yaml file
        - Use kwargs to override values
        """
        self.path = path
        self.section = section

        try:
            # read yaml file
            yaml_content = self._read_yaml(path)

            self._replace_with_environment_variables(yaml_content)

            # add values
            yaml_section = yaml_content[section]
            for key, value in yaml_section.items():
                self[key] = value

            # override values
            self.update({
                key: value
                for key, value in kwargs.items()
            })

        except Exception as ex:
            logger.error(
                f"Failed to read '{section}' section from '{self.path}'. Original: {ex}")
            raise

    def _read_yaml(self, path):
        try:
            with open(path, 'r') as file:
                yaml_content = yaml.safe_load(file)
                return yaml_content
        except FileNotFoundError:
            raise
        except Exception as ex:
            raise YamlParseError(
                f"File '{self.path}' could not be parsed correcty to yaml! Original: {ex}")

    def _set_nested_value(self, yaml_data:dict, keys:List[str], value):
        for key in keys[:-1]:
            yaml_data = yaml_data.setdefault(key, {})
        if value is not None and value:
            yaml_data[keys[-1]] = value

    def _replace_with_environment_variables(self, yaml_content):
        # Pattern to match environment variables with double underscores
        pattern = re.compile(r'(?i)^[a-z][a-z0-9_]*(?:__[a-z][a-z0-9_]*)+$')

        # Process each environment variable
        for key, value in os.environ.items():
            if pattern.match(key):
                # Split the key into parts
                keys = key.lower().split('__')
                # Update the YAML configuration
                self._set_nested_value(yaml_content, keys, value)