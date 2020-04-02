"""
Visualize
"""

import matplotlib.pyplot as plt

from datit.type import *

__all__ = []

_palette = ['#005CAF', '#F596AA', '#FFB11B', '#BEC23F', '#77428F']

def _create_fig(**kwargs) -> Plots:
    return plt.subplots(**kwargs)
