from core import PluginCore
import pandas as pd
from attributes import keyAttributes, sensitiveAttributes, quasiIdentifiers
from utils import utils
from plugins.sharedMethods import dropColumns, generalisationOperations, suppressionOperations

class Kanonymity(PluginCore):
    def __init__(self) -> None:
        super().__init__(1)

    def invoke(self, data: pd.DataFrame) -> pd.DataFrame:
        data = dropColumns(data)
        data = generalisationOperations(data)
        data = suppressionOperations(data)
        data = self.__applyK(data, 15)
        return data

    def isKAnonymized(df, k):
        for index, row in df.iterrows():
            query = ' & '.join([f'{col} == {row[col]}' for col in df.columns])
            rows = df.query(query)
            if rows.shape[0] < k:
                return False
        return True

    def __applyK(self, data: pd.DataFrame, k) -> pd.DataFrame:
        data = data.drop(columns=utils.getListOfAttributes(sensitiveAttributes), errors='ignore')
        availableQuasiIdentifiers = [b for b in list(data) if all(a not in b for a in utils.getListOfAttributes(quasiIdentifiers))]
        grouped = data.groupby(availableQuasiIdentifiers)
        for name, group in grouped:
            if group.shape[0] <= k:
                data.drop(group.index, inplace=True)
        return data

    def x(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.drop(columns=utils.getListOfAttributes(sensitiveAttributes), errors='ignore')
        scale = utils.get_spans(data, data.index)
        finished_partitions = []
        partitions = [data.index]
        while partitions:
            partition = partitions.pop(0)
            spans = utils.get_spans(data, partition, scale)
            for column, span in sorted(spans.items(), key=lambda x:-x[1]):
                lp, rp = self.__split(data, partition, column)
                if not self.__isCompliantWithK(data, lp) or not self.__isCompliantWithK(data, rp):
                    continue
                partitions.extend((lp, rp))
                break
            else:
                finished_partitions.append(partition)
        print(finished_partitions)
        return finished_partitions
        #return data

    def __isCompliantWithK(self, df, partition, k=3):
        if len(partition) < k:
            return False
        return True

    def __split(self, df, partition, column):
        dfp = df[column][partition]
        values = dfp.unique()
        lv = set(values[:len(values)//2])
        rv = set(values[len(values)//2:])
        return dfp.index[dfp.isin(lv)], dfp.index[dfp.isin(rv)]
