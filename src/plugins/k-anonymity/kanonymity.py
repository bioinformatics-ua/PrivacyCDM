from core import PluginCore
import pandas as pd
from attributes import keyAttributes, sensitiveAttributes, quasiIdentifiers
from utils import utils
from plugins.sharedMethods import dropColumns, generalisationOperations, suppressionOperations, getAvailableQuasiIdentifiers, validateClassifications, getEquivalenceClasses
import config

class Kanonymity(PluginCore):
    def __init__(self) -> None:
        super().__init__(1)

    def invoke(self, data: pd.DataFrame) -> (pd.DataFrame, str):
        data = dropColumns(data)
        data = generalisationOperations(data)
        data = suppressionOperations(data)
        data = self.__applyK(data, config.k_anonymity)
        tag = f"k{config.k_anonymity}"
        return data, tag

    def __applyK(self, data: pd.DataFrame, k) -> pd.DataFrame:
        print(f"Applying k-Anonymity with the k value = {k}")
        dataTmp = data
        dataTmp = dataTmp.drop(columns=utils.getListOfAttributes(sensitiveAttributes), errors='ignore')
        
        availableQuasiIdentifiers = getAvailableQuasiIdentifiers(dataTmp)

        dataToGroup = dataTmp
        validateClassifications(dataTmp, availableQuasiIdentifiers)

        equivalenceClasses = getEquivalenceClasses(dataToGroup)
        
        return self.__removeEntries(equivalenceClasses, dataToGroup, data, k)
        
    def __removeEntries(self, equivalenceClasses: dict, dataToGroup: pd.DataFrame, data: pd.DataFrame, k:int) -> pd.DataFrame:
        indexToRemove = list()
        index = 0
        for entry in dataToGroup.values.tolist():
            entry = str(entry)
            if equivalenceClasses[entry] < k:
                indexToRemove.append(index)
            index += 1
        for index, row in data.iterrows():
            if index in indexToRemove:
                data.drop(index, inplace=True)
        return data
