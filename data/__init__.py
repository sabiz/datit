"""
 init
"""
import pandas as pd
import numpy as np

from tqdm import tqdm
from typing import Dict
from typing import List

# from . import sampling
from . import overview

def from_csv(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, engine='python', **kwargs)

def from_csv_all(paths: List[str], **kwargs) -> pd.DataFrame:
    tmp = []
    for p in paths:
        tmp.append(from_csv(p, **kwargs))
    return pd.concat(tmp)

def from_csv_dict(path_dict: Dict[str, str], **kwargs) -> Dict[str, pd.DataFrame]:
    result = {}
    with tqdm(total=len(path_dict)) as p:
        for path in path_dict:
            result[path] = from_csv(path_dict[path], **kwargs)
            p.update(1)
    return result

def format(data: pd.DataFrame, types: Dict[str, str]) -> pd.DataFrame:
    result = data.copy()
    for k in types:
        if types[k][0] == "@":
            f=types[k][1:]
            result[k] = pd.to_datetime(result[k], format=f)
        else:
            result[k] = result[k].astype(types[k])
    return result
