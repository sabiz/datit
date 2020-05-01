"""
Evaluation
"""

import numpy as np
import pandas as pd

from datit.visualize import _visualize as _visu
from datit.visualize._visualize import _palette as palette

__all__ = ['capcurve']


def capcurve(y, y_prob):
    from scipy import integrate
    num_sum = np.sum(y)
    num_count = len(y)
    rate_val = float(num_sum) / float(num_count)
    ideal = np.array([[0, rate_val, 1], [0, 1, 1]])

    y_cap_df = (pd.DataFrame({'y': y, 'yp': y_prob})
                .sort_values('yp', ascending=False)
                .reset_index(drop=True))
    y_cap_df['y_rate'] = np.cumsum(y_cap_df.y)/num_sum
    y_cap_df['x_rate'] = np.arange(num_count)/num_count

    perfect = integrate.simps(ideal[1, :], ideal[0, :])
    model = integrate.simps(y_cap_df.y_rate, y_cap_df.x_rate)
    _random = integrate.simps(y_cap_df.x_rate, y_cap_df.x_rate)
    gini = (model - _random) / (perfect - _random)

    fig, ax = _visu._create_fig()
    ax.plot(ideal[0, :], ideal[1, :],
            color=palette[0], label='Ideal model')
    ax.plot(y_cap_df.x_rate, y_cap_df.y_rate,
            color=palette[1], label='Model')
    ax.plot(y_cap_df.x_rate, y_cap_df.x_rate,
            linestyle='dashed', color=palette[2], label='Random')
    ax_params = {
            "title": f"CAP Curve (Gini index:{gini:.04})",
            "xlabel": "data ratio",
            "ylabel": "positive ratio",
            }
    ax.set(**ax_params)
    ax.legend()
    _visu._plot()