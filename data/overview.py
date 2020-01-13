"""
Overview
"""
from datit import figure
import pandas as pd
import re

def statistic(data: pd.DataFrame) -> pd.DataFrame:
    """
    [data] statistic
    """
    result = pd.DataFrame()

    str_length = []
    min_data = []
    max_data = []
    avg_data = []
    std_data = []
    med_data = []
    mode_data = []
    zero_data = []
    pat = r"^\s+$"
    for c in data:
        data_type = data[c].dtype
        str_length.append(
                max(data[data[c].isnull() == False][c].str.len())
                if data_type == 'object' else '-')
        if data_type == 'object':

            value_counts=data[c].value_counts()
            idx = len(value_counts) -1
            while(re.match(pat, str(value_counts.index[idx])) and idx > 0):
                idx -= 1
            mode_data.append(f'{value_counts.index[0]} ({value_counts.iat[0]})')

            min_data.append('-')
            max_data.append('-')
            avg_data.append('-')
            med_data.append('-')
            std_data.append('-')
            idx = len(value_counts) -1
            while(not re.match(pat, str(value_counts.index[idx])) and idx > -1):
                idx -= 1
            if idx == -1:
                zero_data.append(0)
            else:
                zero_data.append(value_counts.iat[idx])
        elif data_type == 'datetime64[ns]':
            mode_data.append(data[c].mode()[0])
            min_data.append(data[c].min())
            max_data.append(data[c].max())
            avg_data.append(data[c].mean())
            med_data.append(data[c].quantile(0.5))
            std_data.append('-')
            zero_data.append((data[c] == 0).sum())
        else:
            mode_data.append(data[c].mode()[0])
            min_data.append(data[c].min())
            max_data.append(data[c].max())
            avg_data.append(data[c].mean())
            med_data.append(data[c].median())
            std_data.append(data[c].std())
            zero_data.append((data[c] == 0).sum())

    result['COLUMNS'] = data.columns
    result = result.set_index('COLUMNS')
    result['TYPES'] = data.dtypes
    result['STRING_MAX_LENGTH'] = str_length
    result['NULL_COUNT'] = data.isnull().sum()
    result['ZERO_COUNT'] = zero_data
    result['UNIQUE'] = data.nunique()
    result['MODE'] = mode_data
    result['MIN'] = min_data
    result['MAX'] = max_data
    result['AVG'] = avg_data
    result['MED'] = med_data
    result['STD'] = std_data
    return result


def counts(data: pd.DataFrame):
    """
    view counts
    """
    for d in data:
        if data[d].dtype == 'object':
            if len(data[d])*0.9 <= len(data[d].unique()):
                print(f'Too many unique values ignore: {d}')
                continue
            figure.count(data[d])
        else:
            figure.histgram(data[d])

