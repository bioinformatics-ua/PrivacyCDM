from core import PluginCore
import pandas as pd
from attributes import keyAttributes, sensitiveAttributes, quasiIdentifiers
from utils import utils
from plugins.sharedMethods import dropColumns, generalisationOperations, suppressionOperations
import config
import pprint

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
        
        availableQuasiIdentifiers = []
        for attr in utils.getListOfAttributes(quasiIdentifiers):
            if attr in list(dataTmp):
                availableQuasiIdentifiers.append(attr)

        dataToGroup = dataTmp
        emptyData = dataTmp.drop(columns=availableQuasiIdentifiers)
        if not emptyData.empty:
            print("Some attributes are not classified!")
            print(emptyData)
            exit(0)

        counter = {}
        for entry in dataToGroup.values.tolist():
            entry = str(entry)
            if entry not in counter:
                counter[entry] = 0
            counter[entry] += 1

        #saqui para baixo
        indexToRemove = list()
        index = 0
        for entry in dataToGroup.values.tolist():
            entry = str(entry)
            if counter[entry] < l:
                indexToRemove.append(index)
            index += 1

        for index, row in data.iterrows():
            if index in indexToRemove:
                data.drop(index, inplace=True)
        return data

