from core import PluginCore
import pandas as pd
from attributes import keyAttributes, sensitiveAttributes, quasiIdentifiers
from utils import utils
from plugins.sharedMethods import dropColumns, generalisationOperations, suppressionOperations, getAvailableQuasiIdentifiers, validateClassifications, getEquivalenceClasses
import config

class Ldiversity(PluginCore):
    def __init__(self) -> None:
        super().__init__(2)

    def invoke(self, data: pd.DataFrame) -> (pd.DataFrame, str):
        data = dropColumns(data)
        data = generalisationOperations(data)
        data = suppressionOperations(data)
        data = self.__applyL(data, config.l_diversity)
        tag = f"l{config.l_diversity}"
        return data, tag

    def __applyL(self, data: pd.DataFrame, l) -> pd.DataFrame:
        print(f"Applying l-Diversity with the l value = {l}")
        dataTmp = data
        dataTmp = dataTmp.drop(columns=utils.getListOfAttributes(sensitiveAttributes), errors='ignore')
        
        availableQuasiIdentifiers = getAvailableQuasiIdentifiers(dataTmp)

        dataToGroup = dataTmp
        validateClassifications(dataTmp, availableQuasiIdentifiers)

        equivalenceClasses = getEquivalenceClasses(dataToGroup)
        
        indexToRemove = list()
        index = 0
        for entry in dataToGroup.values.tolist():
            entry = str(entry)
            if equivalenceClasses[entry] < l:
                indexToRemove.append(index)
            index += 1

        for index, row in data.iterrows():
            if index in indexToRemove:
                data.drop(index, inplace=True)
        return data

