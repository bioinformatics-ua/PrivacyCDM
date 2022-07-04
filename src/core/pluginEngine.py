from core import PluginActions
from data_manager import DataManager

class PluginEngine:
    def __init__(self, **args) -> None:
        self.actions = PluginActions(args['options'])
        self.dataLocation = args['options']['dataLocation']
        self.exportLocation = args['options']['exportLocation']
        self.delimiter = args['options']['delimiter']

    def start(self) -> None:
        self.__reloadPlugins()
        self.__invokePlugins()

    def __reloadPlugins(self) -> None:
        self.actions.discover(True)

    def __invokePlugins(self) -> None:
        data = DataManager.loadData(self.dataLocation, self.delimiter)
        for module in self.actions.modules:
            plugin = self.actions.register(module)
            anonimiser = self.actions.hook(plugin)
            data = anonimiser(data=data)
        DataManager.exportData(data, self.exportLocation, self.dataLocation, self.delimiter)
