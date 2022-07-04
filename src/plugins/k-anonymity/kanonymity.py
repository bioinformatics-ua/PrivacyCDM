from core import PluginCore
import pandas as pd
from attributes import keyAttributes, sensitiveAttributes, quasiIdentifiers
from utils import utils
from plugins.sharedMethods import dropColumns, generalisationOperations, suppressionOperations
import config

class Kanonymity(PluginCore):
    def __init__(self) -> None:
        super().__init__(1)

    def invoke(self, data: pd.DataFrame) -> pd.DataFrame:
        data = dropColumns(data)
        data = generalisationOperations(data)
        data = suppressionOperations(data)
        data = self.__applyK(data, config.k_anonymity)
        return data

    def __applyK(self, data: pd.DataFrame, k) -> pd.DataFrame:
        print(f"Applying k-Anonymity with the k value = {k}")
        data = data.drop(columns=utils.getListOfAttributes(sensitiveAttributes), errors='ignore')
        availableQuasiIdentifiers = [b for b in list(data) if all(a not in b for a in utils.getListOfAttributes(quasiIdentifiers))]
        grouped = data.groupby(availableQuasiIdentifiers)
        for name, group in grouped:
            if group.shape[0] <= k:
                data.drop(group.index, inplace=True)
        return data
