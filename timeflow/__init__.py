from abc import ABCMeta, abstractmethod

class StepBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def timeseries(self): pass

    @abstractmethod
    def stream(self): pass


class File(StepBase):
    """Simple class for handling file reading in a timeflow"""
    def __init__(self, filename, **kwargs):
        self.filename = filename

    def timeseries(self):
        raise NotImplementedError('file routines don\'t provide timeseries. '\
            'Try File.stream() for a file object.')

    def stream(self):
        return open(self.filename)


class CSV(StepBase):
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


class Threshold(StepBase):
    def __init__(self, step_meta, data_from):
        print data_from.timeseries()

    def timeseries(self): pass

    def stream(self): pass
