import os
from importlib import import_module
from typing import List, Any, Dict, Union, Optional
from core import Registry, PluginCore
from utils import filterPluginsPaths, readConfiguration, FileSystem, PluginConfig
import pkg_resources
from dacite import from_dict
from pkg_resources import Distribution

class PluginActions:
    modulesWithPosition: List[type]
    modules: List[type]

    def __init__(self, options: Dict) -> None:
        self.modulesWithPosition = list()
        self.modules = list()
        self.pluginsPackage: str = options['directory']
        self.selectedPlugins: dict = options['plugins']

    def __checkStateOfLoadedPlugin(self, pluginModule: Any):
        if len(Registry.pluginRegistries) > 0:
            latestModule = Registry.pluginRegistries[-1]
            latestModuleName = latestModule.__module__
            currentModuleName = pluginModule.__name__
            if currentModuleName == latestModuleName:
                print(f'Successfully imported module `{currentModuleName}`')
                self.modulesWithPosition.append((latestModule().getPosition(), latestModule))
            else:
                print(f'Expected to import `{currentModuleName}`')
            Registry.pluginRegistries.clear()
        else:
            print(f'No plugin found for module: {pluginModule}')
    
    def setupPluginConfiguration(self, packageName, moduleName) -> Optional[str]:
        modulePath = os.path.join(FileSystem.getPluginsDirectory(), moduleName)
        if os.path.isdir(modulePath):
            print(f'Checking if configuration file exists for module: {moduleName}')
            pluginConfig: Optional[PluginConfig] = readConfiguration(modulePath)
            if pluginConfig is not None:
                if pluginConfig.name in self.selectedPlugins:
                    return pluginConfig.runtime.main
                else:
                    return None
            else:
                print(f'No configuration file exists for module: {moduleName}')
        print(f'Module: {moduleName} is not a directory, skipping scanning phase')
        return None
    
    def __sortPlugins(self) -> None:
        self.modulesWithPosition.sort(key=lambda y: y[0])
        for index, module in self.modulesWithPosition:
            self.modules.append(module)

    def __searchingPlugins(self, pluginsPath: List[str], packageName: str):
        for directory in pluginsPath:
            entry_point = self.setupPluginConfiguration(packageName, directory)
            if entry_point is not None:
                pluginName, _ = os.path.splitext(entry_point)
                importTargetModule = f'.{directory}.{pluginName}'
                module = import_module(importTargetModule, packageName)
                self.__checkStateOfLoadedPlugin(module)
            else:
                print(f'No valid plugin found in {packageName}')
        self.__sortPlugins()

    def discover(self, reload: bool):
        if reload:
            self.modules.clear()
            Registry.pluginRegistries.clear()
            print(f'Searching for plugins under package {self.pluginsPackage}')
            pluginsPath = filterPluginsPaths(self.pluginsPackage)
            packageName = os.path.basename(os.path.normpath(self.pluginsPackage))
            self.__searchingPlugins(pluginsPath, packageName)

    @staticmethod
    def register(module: type) -> PluginCore:
        return module()

    @staticmethod
    def hook(plugin: PluginCore):
        return plugin.invoke
