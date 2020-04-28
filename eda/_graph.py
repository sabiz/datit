"""
eda graph
"""
import numpy as np
import pandas as pd
import seaborn as sns

from typing import Optional

from datit.visualize import _visualize as _visu
from datit.visualize._visualize import _palette as palette


def check_normal_dist(x: pd.Series):
    from scipy import stats
    from scipy.stats import norm
    if x.dtype == 'object':
        return
    fig, ax = _visu._create_fig(ncols=2)
    sns.distplot(x, fit=norm, ax=ax[0])
    stats.probplot(x, plot=ax[1])
    _visu._plot()


def scatter_plot(x: pd.Series, y: pd.Series):
    fig, ax = _visu._create_fig()
    ax.scatter(x, y)
    ax.set(title=f'Scatter {x.name} x {y.name}',
           xlabel=x.name, ylabel=y.name)
    _visu._plot()


def violin_plot(x: pd.Series, y: pd.Series):
    fig, ax = _visu._create_fig()
    sns.violinplot(x=x, y=y, scale='width', inner='quartile')
    ax.set(title=f'Violin {x.name} x {y.name}',
           xlabel=x.name, ylabel=y.name)
    _visu._plot()


def box_plot(x: pd.Series, y: pd.Series):
    fig, ax = _visu._create_fig()
    sns.boxplot(x=x, y=y)
    sns.stripplot(x=x, y=y, color='black', size=2, jitter=1, alpha=0.5)
    ax.set(title=f'Box {x.name} x {y.name}',
           xlabel=x.name, ylabel=y.name)
    _visu._plot()


def density_2d_plot(x: pd.Series, y: pd.Series, band_width: Optional[float] = None):
    band = band_width
    if x.dtype == 'object' or y.dtype == 'object':
        print("Ignore non number type")
        return
    if band is None:
        band = 'scott'
    fig, ax = _visu._create_fig()
    sns.kdeplot(x, y, shade=True, ax=ax, bw=band)
    ax.set(title=f'Density {x.name} x {y.name} (band width:{band})',
           xlabel=x.name, ylabel=y.name)
    _visu._plot()


def density_plot(data: pd.Series, band_width: Optional[float] = None):
    band = band_width
    if data.dtype == 'object':
        print("Ignore non number type")
        return
    if band is None:
        band = 'scott'
    fig, ax = _visu._create_fig()
    sns.kdeplot(data, shade=True, ax=ax, bw=band)
    ax.set(title=f'Density {data.name}(band width:{band})',
           xlabel=data.name, ylabel='Frequency')
    _visu._plot()


def histgram(data: pd.Series, bins: Optional[int] = None):
    if data.dtype == 'object':
        print("Ignore non number type")
        return
    bin_number = bins
    if bin_number is None:
        bin_number = int(1 + np.log2(len(data)))
    fig, ax = _visu._create_fig()
    ax.hist(data, bins=bin_number)
    ax.set(title=f'Histgram {data.name}(bin:{bin_number})',
           xlabel=data.name, ylabel='Frequency')
    _visu._plot()


def pareto(data: pd.Series):
    """
    Plot pareto chart
    """
    if data.dtype != 'object':
        return
    fig, ax = _visu._create_fig()
    counts = data.value_counts()
    ax.bar(counts.index, counts.values, label='count')
    ax.set(title=f'Pareto: {counts.name}')
    ax2 = ax.twinx()
    ratio = counts / counts.sum()
    ax2.plot(ratio.index, ratio.cumsum(), label='ratio', c=palette[1])
    ax2.set(ylim=(0, 1.05))
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    _visu.plt.legend(h1+h2, l1+l2)
    _visu._plot()


def value_count(data: pd.Series):
    """
    Plot value counts
    """
    fig, ax = _visu._create_fig()
    counts = data.value_counts()
    ax.bar(counts.index, counts.values)
    ax.set(title=f'Value Count: {counts.name}')
    _visu._plot()
