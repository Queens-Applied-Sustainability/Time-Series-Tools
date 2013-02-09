from abc import ABCMeta, abstractmethod
import pandas as pd
from timeflow import data

class RoutineBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, label, data_from, **setup_kwargs):
        self.label = label
        self._data_source = data.Connector(**data_from)
        data.Connector.register(label, self)
        self.setup(**setup_kwargs)

    @abstractmethod
    def setup(self):
        pass

    def data():
        doc = "The data property."
        def fget(self):
            if not hasattr(self, '_data'):
                self._data = self._data_source.get()
            return self._data
        def fset(self, value):
            self._data = value
        def fdel(self):
            del self._data
        return locals()
    data = property(**data())

    @abstractmethod
    def operate(self, **kwargs):
        pass

    def get_new(self, **kwargs):
        columns = self.operate(**kwargs)
        return columns if columns is not None else []

    def get_all(self, **kwargs):
        new_columns = self.get_new(**kwargs)
        if any(new_columns):
            self.data[self.label] = new_columns
        return self.data

    def get_if(self, **kwargs):
        compressed = self.data[self.get_new(**kwargs)]
        return compressed
