"""
Explore
"""
import numpy as np
import pandas as pd
import re

from ._graph import value_count
from ._graph import pareto
from ._graph import histgram
from ._graph import density_plot
from ._graph import density_2d_plot
from ._graph import box_plot
from ._graph import violin_plot
from ._graph import scatter_plot
from ._graph import check_normal_dist

__all__ = (['summary', 'simple_report', 'corr'] +
           ['value_count', 'pareto', 'histgram',
            'density_plot', 'density_2d_plot', 'box_plot',
            'violin_plot', 'scatter_plot', 'check_normal_dist'])


def corr(data: pd.DataFrame, target: str):
    """
    !! retuen target mean, if dtype is object
    """
    results = {"name": [], "value": []}
    for c in data.columns:
        if c == target:
            continue
        if data[c].dtype == "object":
            tmp = data.groupby(c).mean()[target].to_dict()
            for t in tmp:
                results["name"].append(f"{c} ({t})")
                results["value"].append(tmp[t])
            continue
        results["name"].append(c)
        results["value"].append(np.corrcoef(data[c], data[target])[0, 1])
    return pd.DataFrame(results)


def simple_report(data: pd.DataFrame):
    from pandas_profiling import ProfileReport
    import sys
    inJupyter = sys.argv[-1].endswith('json')
    report = ProfileReport(data, title='Report', html={'style': {'full_width': True}})
    if inJupyter:
        return report.to_notebook_iframe()
    else:
        return report.to_file(output_file='simple_report.html')


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

            value_counts = data[c].value_counts()
            idx = len(value_counts) -1
            while(re.match(pat, str(value_counts.index[idx])) and idx > 0):
                idx -= 1
            mode_data.append(f'{value_counts.index[0]} ({value_counts.iat[0]})')

            min_data.append('-')
            max_data.append('-')
            avg_data.append('-')
            med_data.append('-')
            std_data.append('-')
            idx = len(value_counts) - 1
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
