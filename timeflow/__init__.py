from abc import ABCMeta, abstractmethod
from numpy import ndarray

from timeflow.routine_bases import RoutineBase


class MapColumns(RoutineBase):
    pass


class BoolFilter(RoutineBase):
    cmp_trans = {
        '<':  lambda l, r: l < r,
        '<=': lambda l, r: l <= r,
        '==': lambda l, r: l == r,
        '>=': lambda l, r: l >= r,
        '>':  lambda l, r: l > r,
        '!=': lambda l, r: l != r,
    }

    def __init__(self, column, operator, value, **kwargs):
        super(BoolFilter, self).__init__(**kwargs)
        self.thresh_column = column
        self.thresh_operator = operator
        self.thresh_value = value

    def operate(self):
        column = self.data[self.thresh_column]
        result = self.cmp_trans[self.thresh_operator](column, self.thresh_value)
        return result


if __name__ == '__main__':

    imp = CSVImport(label='import', data_from='../time-series.csv')

    bfilter = BoolFilter(label='bfilt', data_from='import',
                         column='temperature', operator='<', value=15.3)

    print imp.get_all()
    print bfilter.get_if()
    print bfilter.data.dtype

