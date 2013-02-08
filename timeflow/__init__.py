from abc import ABCMeta, abstractmethod
from numpy import ndarray


class DataConnector(ndarray):
    """"The connector for sequences of routines.
    Attaches to the acting routine, and references another routine by label.
    """
    routine_registry = {} # mutable struture is the same for all instances

    def __init__(self, source, merge=None, **modifiers):
        self.source_label = source
        self.merge = merge
        self.modifiers = modifiers

    @classmethod
    def register(cls, label, routine):
        if label in cls.routine_registry:
            raise KeyError('Routine label conflict for {}.'.format(label))
        cls.routine_registry[label] = routine

    def get(self):
        # handle merges and all that...
        source_routine = self.routine_registry[self.source_label]
        source_data = source_routine.get_all()
        return source_data


class RoutineBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, label, data_from, merge, **modifiers):
        self._data_source = DataConnector(data_from, **modifiers)
        DataConnector.register(label, self)

    @property
    def data(self):
        return self._data_source.get()

    @abstractmethod
    def operate(self, *args, **kwargs):
        pass

    def operate_if(self, *args, **kwargs):
        """Be optimistic that the operate method just happens to return a
        suitable boolean column"""
        condition = self.operate(self, *args, **kwargs)
        return condition

    def get_new(self, *args, **kwargs):
        columns = self.operate(*args, **kwargs)
        return column

    def get_all(self, *args, **kwargs):
        columns = self.get_new(*args, **kwargs)
        full = self.data # link the data and new columns
        return full

    def get_if(self, *args, **kwargs):
        condition = self.operate_if(*args, **kwargs)
        compressed = self.data.compress(condition)
        return compressed



class BoolFilter(RoutineBase):
    cmp_trans = {
        '<':  lambda l, r: l < r,
        '<=': lambda l, r: l <= r,
        '==': lambda l, r: l == r,
        '>=': lambda l, r: l >= r,
        '>':  lambda l, r: l > r,
        '!=': lambda l, r: l != r,
    }

    def __init__(self, data_from, column, rule, value):
        super(BoolFilter, self).__init__(data_from)
        self.thresh_column = column
        self.thresh_rule = rule
        self.thresh_value = value

    def operate(self):
        column = self.data[self.thresh_column]
        result = cmp_trans[self.thresh_rule](self.thresh_value, column)
        return result


class File(RoutineBase):
    """Simple class for handling file reading in a timeflow"""
    def __init__(self, filename, **kwargs):
        self.filename = filename

    def timeseries(self):
        raise NotImplementedError('This file routine does not provide a '\
            'timeseries directly. File.stream() will give you a file object.')

    def stream(self):
        return open(self.filename)


class CSV(File):
    def __init__(self, step_meta, data_from):
        self.data_from = data_from.stream

    def timeseries(self):
        from numpy import genfromtxt
        csv_config = {
            'delimiter': ',',
            'names': True,
            'dtype': None,
        }
        return genfromtxt(self.data_from(), **csv_config)

    def stream(self): pass


