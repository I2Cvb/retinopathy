"""
The :mod:`data_balancing.data_load` module includes utilities to load and adapt datasets,
that takes advantage of :mod:`sklearn.datasets`.
"""

from .base import get_data_home
from datasets.oct import dummy

__all__ = ['get_data_home',
           'dummy',
          ]


