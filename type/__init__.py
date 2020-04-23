"""
Type
"""

from typing import Union
from typing import List
from typing import Tuple

from matplotlib.figure import Figure
from matplotlib.axes import Axes

Plots = Union[Tuple[Figure, List[Axes]], Tuple[Figure, Axes]]

__all__ = ['List', 'Plots']
