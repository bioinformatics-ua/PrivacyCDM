import os
from config import cdmSchemaPath, pluginsPath
from utils import FileSystem, PluginConfig
from dacite import from_dict
from typing import List, Dict, Union, Optional
import yaml

__IGNORE_LIST = ['__pycache__', '__init__.py', 'sharedMethods.py']
def __filterUnwantedDirectories(name: str) -> bool:
    return not __IGNORE_LIST.__contains__(name)

def filterPluginsPaths(pluginsPackage) -> List[str]:
    return list(filter(__filterUnwantedDirectories, os.listdir(pluginsPackage)))

def readConfiguration(modulePath) -> Optional[PluginConfig]:
	try:
		pluginConfigData = FileSystem.loadConfiguration('plugin.yaml', modulePath)
		pluginConfig = from_dict(data_class=PluginConfig, data=pluginConfigData)
		return pluginConfig
	except FileNotFoundError as e:
		print('Unable to read configuration file', e)
	except (NameError) as e:
		print('Unable to parse plugin configuration to data class', e)
	return None
		
def readFields() -> None:
	with open(cdmSchemaPath, 'r') as f:
		lines = f.readlines()
	for line in lines:
		data = line.split(",")
		if len(data) > 2:
			print(data[0],data[1])

def processAttributes(listOfAttributes: list) -> dict:
	dictOfAttributes = {}
	for table, field in listOfAttributes:
		table = table.lower()
		if table not in dictOfAttributes:
			dictOfAttributes[table] = []
		dictOfAttributes[table].append(field.lower())
	return dictOfAttributes

def attibutesToLatexTable(dictOfAttributes: dict) -> None:
	for table in dictOfAttributes:
		tableToPrint = table.replace("_", "\\_")
		print("\t" + tableToPrint, end = ' & ')
		tableFields = ""
		for field in dictOfAttributes[table]:
			tableFields += field
			tableFields += ", "
		tableFields = tableFields[:-2]
		tableFields += " \\\\  \git \hline"
		tableFields = tableFields.replace("_", "\\_")
		print(tableFields)

def getListOfAttributes(listOfAttributes: list) -> list:
	newListOfAttributes = set()
	for table, field in listOfAttributes:
		newListOfAttributes.add(field) 
	return list(newListOfAttributes)

def get_spans(df, partition, scale=None):
    spans = {}
    for column in df.columns:
        span = len(df[column][partition].unique())
        if scale is not None:
            span = span/scale[column]
        spans[column] = span
    return spans