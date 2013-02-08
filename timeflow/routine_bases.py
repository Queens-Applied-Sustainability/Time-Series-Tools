

class RoutineBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, label, data_from, source_modifiers=None):
        self._data_source = DataConnector(data_from, source_modifiers)
        DataConnector.register(label, self)

    @property
    def data(self):
        return self._data_source.get()

    @abstractmethod
    def operate(self, **kwargs):
        pass

    def operate_if(self, **kwargs):
        """Be optimistic that the operate method just happens to return a
        suitable boolean column"""
        condition = self.operate(**kwargs)
        return condition

    def get_new(self, **kwargs):
        columns = self.operate(**kwargs)
        return columns

    def get_all(self, **kwargs):
        columns = self.get_new(**kwargs)
        full = self.data # link the data and new columns
        return full

    def get_if(self, **kwargs):
        condition = self.operate_if(**kwargs)
        compressed = self.data.compress(condition)
        return compressed