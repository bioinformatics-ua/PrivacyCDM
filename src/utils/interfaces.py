from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PluginRunTimeOption(object):
    main: str
    tests: Optional[List[str]]

@dataclass
class PluginConfig:
    name: str
    creator: str
    runtime: PluginRunTimeOption
    description: str
    version: str