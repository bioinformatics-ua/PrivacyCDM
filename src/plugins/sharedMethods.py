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