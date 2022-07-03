import os
from config import pluginsPath
from typing import Optional
import yaml

class FileSystem:
    @staticmethod
    def getPluginsDirectory() -> str:
        return pluginsPath

    @staticmethod
    def loadConfiguration(name: str, config_directory: Optional[str]) -> dict:
        with open(os.path.join(config_directory, name)) as file:
            input_data = yaml.safe_load(file)
        return input_data
