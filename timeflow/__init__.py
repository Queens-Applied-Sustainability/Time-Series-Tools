from abc import ABCMeta, abstractmethod
from numpy import ndarray


class DataConnector(object):
    """"The connector for sequences of routines.
    Attaches to the acting routine, and references another routine by label.
    """
    routine_registry = {} # mutable struture is the same for all instances

    def __init__(self, source, **source_modifiers):
        self.source_label = source
        self.source_modifiers = source_modifiers

    @classmethod
    def register(cls, label, routine):
        if label in cls.routine_registry:
            raise KeyError('Routine label conflict for {}.'.format(label))
        cls.routine_registry[label] = routine

    def get(self):
        # handle merges and all that...
        try:
            source_routine = self.routine_registry[self.source_label]
        except KeyError:
            raise KeyError('The routine "{}" is not registered. '
                'Registered routines: {}'.format(self.source_label,
                ', '.join(self.routine_registry.keys())))
        source_data = source_routine.get_all()
        return source_data.get_all()


class RoutineBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, label, data_from, **source_modifiers):
        self._data_source = DataConnector(data_from, **source_modifiers)
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

    def __init__(self, column, operator, value, **kwargs):
        super(BoolFilter, self).__init__(**kwargs)
        self.thresh_column = column
        self.thresh_operator = operator
        self.thresh_value = value

    def operate(self):
        column = self.data[self.thresh_column]
        result = cmp_trans[self.thresh_operator](self.thresh_value, column)
        return result


class CSVImport(RoutineBase):
    """This import class expects a file-like stream as its source"""
    def __init__(self, map=None, const=None, **kwargs):
        super(CSVImport, self).__init__(**kwargs)
        self.map = map
        self.const = const

    def operate(self):
        return ndarray()


if __name__ == '__main__':

    imp = CSVImport(label='import', data_from='File',
                    source_modifiers={'filename': 'time-series.csv'})

    bfilter = BoolFilter(label='bfilt', data_from='import',
                         column='temperature', operator='<', value=15.3)

    print bfilter.data


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


