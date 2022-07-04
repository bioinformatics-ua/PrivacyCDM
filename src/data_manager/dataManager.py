import pandas as pd
from os import path

class DataManager:
    @staticmethod
    def loadData(location: str, delimiter: str) -> pd.DataFrame:
        data = pd.read_csv(location, delimiter=delimiter)
        return data

    @staticmethod
    def exportData(data: pd.DataFrame, location: str, source: str, delimiter: str) -> None:
        name = "anonymised_" + source.split("/")[-1]
        data.to_csv(path.join(location, name), sep=delimiter)