"""
blah blah blah
"""

import logging
import pandas as pd
from timeflow.routine_bases import RoutineBase


class ConstantColumns(RoutineBase):
    """Add new columns filled with a constant value."""
    def setup(self, constants):
        self.constants = constants

    def operate(self):
        cols = pd.DataFrame(index=self.data.index)
        for label, value in self.constants.items():
            if label in self.data:
                logging.warning('Overwriting {} with {}s.'.format(label, value))
            cols[label] = pd.Series(value)
        return cols


class Rename(RoutineBase):
    """does exactly what you'd expect"""
    def setup(self, **rename_kwargs):
        self.rename_kwargs = rename_kwargs

    def operate(self):
        renamed = self.data.rename(**self.rename_kwargs)
        self.data = renamed


class BooleanFilter(RoutineBase):
    """Filter rows against a boolean condition for a column."""
    def setup(self, column, operator, value):
        self.filter_column = column
        self.filter_op = operator
        self.filter_value = value

    def operate(self):
        bool_op_map = {
            '<': lambda l, r: l < r,
            '<=': lambda l, r: l <= r,
            '==': lambda l, r: l == r,
            '>=': lambda l, r: l >= r,
            '>': lambda l, r: l > r,
            '!=': lambda l, r: l != r,
        }
        column = self.data[self.filter_column]
        result = bool_op_map[self.filter_op](column, self.filter_value)
        return result
