"""
 init
"""

from ._data import *


# def format(data: pd.DataFrame, types: Dict[str, str]) -> pd.DataFrame:
#     result = data.copy()
#     for k in types:
#         if types[k][0] == "@":
#             f=types[k][1:]
#             result[k] = pd.to_datetime(result[k], format=f)
#         else:
#             result[k] = result[k].astype(types[k])
#     return result
