from core import Registry
import string

class PluginCore(object, metaclass=Registry):
    def __init__(self) -> None:
        pass

    def invoke(self, **args) -> string:
        pass