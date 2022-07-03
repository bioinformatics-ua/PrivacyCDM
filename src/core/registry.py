from typing import List

class Registry(type):
    pluginRegistries: List[type] = list()

    def __init__(cls, name, bases, attrs):
        super().__init__(cls)
        if name != 'PluginCore':
            Registry.pluginRegistries.append(cls)