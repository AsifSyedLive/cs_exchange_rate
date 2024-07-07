import os
import json
from dotenv import load_dotenv
from config import *

class ConfigLoader:
    def __init__(self, env_file='.env', common_config_file='config_common.json', module_config_file=None):
        self.env_file = env_file
        self.common_config_file = os.path.join(os.path.dirname(__file__), '..', 'config', common_config_file)
        if module_config_file:
            self.module_config_file = os.path.join(os.path.dirname(__file__), '..', 'config', module_config_file)

        self.env_config = {}
        self.common_config = {}
        self.module_config = {}

        self.load_env_config()
        self.load_json_config(self.common_config_file, self.common_config)
        if module_config_file:
            self.load_json_config(self.module_config_file, self.module_config)

    def load_env_config(self):
        load_dotenv(self.env_file)
        self.env_config = {
            'BASE_PATH': os.getenv('BASE_PATH'),
            'API_KEY': os.getenv('API_KEY'),
            'LOG_DIR': os.getenv('LOG_DIR'),
            'LOG_FILE': os.getenv('LOG_FILE')
        }

    def load_json_config(self, config_file, config_dict):
        try:
            with open(config_file, 'r') as file:
                config_dict.update(json.load(file))
        except FileNotFoundError:
            print(f"Config file '{config_file}' not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON config file '{config_file}'.")

    def get_env_variables(self):
        return self.env_config

    def get_common_config(self):
        return self.common_config

    def get_module_config(self):
        return self.module_config


