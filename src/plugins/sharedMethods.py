import pandas as pd
from attributes import keyAttributes, sensitiveAttributes, quasiIdentifiers
from utils import utils

def dropColumns(data: pd.DataFrame) -> pd.DataFrame:
    data = data.loc[:, ~data.columns.str.replace("(\.\d+)$", "").duplicated()]
    data = data.drop(columns=utils.getListOfAttributes(keyAttributes), errors='ignore')
    return data
    
def generalisationOperations(data: pd.DataFrame) -> pd.DataFrame:
    return data
        
def suppressionOperations(data: pd.DataFrame) -> pd.DataFrame:
    return data

def getAvailableQuasiIdentifiers(data: pd.DataFrame) -> list:
    availableQuasiIdentifiers = []
    for attr in utils.getListOfAttributes(quasiIdentifiers):
        if attr in list(data):
            availableQuasiIdentifiers.append(attr)
    return availableQuasiIdentifiers

def validateClassifications(data: pd.DataFrame, availableQuasiIdentifiers: list) -> None:
    emptyData = data.drop(columns=availableQuasiIdentifiers)
    if not emptyData.empty:
        print("Some attributes are not classified!")
        print(emptyData)
        exit(0)

def getEquivalenceClasses(data: pd.DataFrame) -> dict:
    counter = {}
    for entry in data.values.tolist():
        entry = str(entry)
        if entry not in counter:
            counter[entry] = 0
        counter[entry] += 1
    return counter