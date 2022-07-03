import os
from config import cdmSchemaPath, pluginsPath
from typing import List, Dict, Union, Optional
import yaml

__IGNORE_LIST = ['__pycache__', '__init__.py']
def __filterUnwantedDirectories(name: str) -> bool:
    return not __IGNORE_LIST.__contains__(name)

def filterPluginsPaths(pluginsPackage) -> List[str]:
    return list(filter(__filterUnwantedDirectories, os.listdir(pluginsPackage)))

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
