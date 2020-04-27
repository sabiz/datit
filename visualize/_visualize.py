"""
Visualize
"""

import seaborn as sns
import matplotlib.pyplot as plt

from datit.type import *

__all__ = []

_palette = [
        '#005CAF', '#F596AA', '#FFB11B', '#BEC23F', '#77428F',
        '#E16B8C', '#F05E1C', '#FFC408', '#5DAC81', '#70649A',
        ]

sns.set_style('whitegrid')
sns.set_context(rc={'patch.linewidth': 0.0})
sns.set_palette(_palette)


def _create_fig(**kwargs) -> Plots:
    return plt.subplots(**kwargs)


def _plot():
    plt.tight_layout()
    plt.plot()
