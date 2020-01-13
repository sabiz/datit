"""
 init
"""
from typing import Optional

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# import matplotlib as mpl
# print(mpl.matplotlib_fname())
sns.set(font='HackGen')  # For japanese plot

def count(data: pd.Series):
    plt.figure(figsize=(30, 10))
    if len(data.unique()) > 15:
        plt.xticks(rotation=70)
    plt.title(f"{data.name} Count")
    plt.xlabel(data.name)
    plt.ylabel('count')
    sns.countplot(data, order=list(data.value_counts(sort=True).index))
    plt.show()

def histgram(data: pd.Series, bins: Optional[int] = None):
    bin_number = bins
    fig_data = data
    if bin_number is None:
        bin_number = int(1 + np.log2(len(data)))

    plt.figure(figsize=(30, 10))
    plt.title(f"{data.name} Histgram")
    plt.xlabel(data.name)
    plt.ylabel('count')
    sns.distplot(fig_data, kde=False, rug=False, bins=bin_number)
    plt.show()


