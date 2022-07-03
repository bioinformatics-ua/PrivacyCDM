from core import PluginActions

class PluginEngine:
    def __init__(self, **args) -> None:
        self.actions = PluginActions(args['options'])

    def start(self) -> None:
        self.__reloadPlugins()
        self.__invokePlugins()

    def __reloadPlugins(self) -> None:
        self.actions.discover(True)

    def __invokePlugins(self) -> None:
        for module in self.actions.modules:
            plugin = self.actions.register(module)
            delegate = self.actions.hook(plugin)
            print(plugin)#change this
