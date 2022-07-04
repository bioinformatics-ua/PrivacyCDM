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
        
        return self.__removeEntries(equivalenceClasses, dataToGroup, data, l)
        
    def __removeEntries(self, equivalenceClasses: dict, dataToGroup: pd.DataFrame, data: pd.DataFrame, l:int) -> pd.DataFrame:
        indexToRemove = list()
        indexToAnalise = list()
        dictIndexToAnalise = dict()
        index = 0
        for entry in dataToGroup.values.tolist():
            entry = str(entry)
            #If no l entries for the equivalence class, so no l different attributes 
            if equivalenceClasses[entry] < l: 
                indexToRemove.append(index)
            else:
                if entry not in dictIndexToAnalise:
                    dictIndexToAnalise[entry] = []
                dictIndexToAnalise[entry].append(index)
                indexToAnalise.append(index)
            index += 1

        counterSA = dict()
        removeSA = dict()
        for index, row in data.iterrows():
            if index in indexToAnalise and index not in indexToRemove:
                for entry in dictIndexToAnalise:
                    if index in dictIndexToAnalise[entry]: #encotnrei a entrada certa par ao index
                        if len(dictIndexToAnalise[entry]) < l: #nem vale a pena continuar
                            for x in dictIndexToAnalise[entry]:
                                indexToRemove.append(x)
                        else:
                            if entry not in counterSA:
                                counterSA[entry] = set()
                            counterSA[entry].add(str(row.tolist()))
                            if entry not in removeSA:
                                removeSA[entry] = []
                            removeSA[entry].append(index)

        for entry in counterSA:
            if len(counterSA[entry]) < l: #marcar para remover
                for x in removeSA[entry]:
                    indexToRemove.append(x)

        for index, row in data.iterrows():
            if index in indexToRemove:
                data.drop(index, inplace=True)
        return data

