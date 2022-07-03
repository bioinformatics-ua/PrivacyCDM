from core import Registry
import string

class PluginCore(object, metaclass=Registry):
    def __init__(self, position: int) -> None:
        self.position = position

    def getPosition(self) -> int:
        return self.position
        
    def invoke(self, **args) -> string:
        pass