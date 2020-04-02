"""
Explore
"""
import numpy as np
import pandas as pd
import re

from datit.visualize import _visualize as _visu
from datit.visualize._visualize import _palette as plt

__all__ = ['summary', 'value_count', 'pareto']

def pareto(data: pd.Series):
    """
    Plot pareto chart
    """
    if data.dtype != 'object':
        return
    fig, ax = _visu._create_fig()
    counts = data.value_counts()
    ax.bar(counts.index, counts.values, label='count' ,color=plt[0])
    ax.set(title=f'Pareto: {counts.name}')
    ax2 = ax.twinx()
    ratio = counts / counts.sum()
    ax2.plot(ratio.index, ratio.cumsum(), label='ratio', c=plt[1])
    ax2.set(ylim=(0, 1.05))
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    _visu.plt.tight_layout()
    _visu.plt.legend(h1+h2, l1+l2)
    _visu.plt.plot()


def value_count(data: pd.Series):
    """
    Plot value counts
    """
    fig, ax = _visu._create_fig()
    counts = data.value_counts()
    ax.bar(counts.index, counts.values, color=plt[0])
    ax.set(title=f'Value Count: {counts.name}')
    _visu.plt.tight_layout()
    _visu.plt.plot()


def summary(data: pd.DataFrame) -> pd.DataFrame:
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
            tmp = data[c]
            if data_type == np.float16:
                tmp = data[c].astype(np.float32)
            mode_data.append(tmp.mode()[0])
            min_data.append(tmp.min())
            max_data.append(tmp.max())
            avg_data.append(tmp.mean())
            med_data.append(tmp.median())
            std_data.append(tmp.std())
            zero_data.append((tmp == 0).sum())

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
