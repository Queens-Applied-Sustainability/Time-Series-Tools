"""
blah blah blah
"""

import logging
import pandas as pd
from timeflow.routine_bases import RoutineBase


class Passthrough(RoutineBase):
    """Do nothing."""
    def setup(self):
        pass

    def operate(self):
        logging.debug('operating passthrough {}'.format(self.label))
        return self.data


class PickColumns(RoutineBase):
    """Trim the table down to the specified columns"""
    def setup(self, columns):
        self.columns = columns

    def operate(self):
        logging.debug('operating pickcolumns {}'.format(self.label))
        raise NotImplementedError


class ConstantColumns(RoutineBase):
    """Add new columns filled with a constant value."""
    def setup(self, constants):
        self.constants = constants

    def operate(self):
        logging.debug('operating constantcolumns {}'.format(self.label))
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
        logging.debug('operating rename {}'.format(self.label))
        renamed = self.data.rename(**self.rename_kwargs)
        return renamed


class BooleanFilter(RoutineBase):
    """Filter rows against a boolean condition for a column."""
    def setup(self, new_column, filter_column, operator, value):
        self.new_column = new_column
        self.filter_column = filter_column
        self.filter_op = operator
        self.filter_value = value

    def operate(self):
        logging.debug('operating booleanfilter {}'.format(self.label))
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
        result.name = self.new_column
        return result

