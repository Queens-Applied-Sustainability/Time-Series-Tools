from abc import ABCMeta, abstractmethod
import logging
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
            logging.debug('getting from within' + self.label)
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
