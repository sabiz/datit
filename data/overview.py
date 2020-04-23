"""
Overview
"""
from datit import figure



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

