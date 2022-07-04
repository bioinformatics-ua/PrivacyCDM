from core import PluginCore
import pandas as pd

class Ldiversity(PluginCore):
    def __init__(self) -> None:
        super().__init__(2)

    def invoke(self, data) -> str:
        print(f'Command: {data}')
        return "diversity"
