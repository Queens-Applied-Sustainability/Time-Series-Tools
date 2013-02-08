"""
do stuff with data
"""

class LabeledRegistry(dict):
    """like a dict, but if a keyerror is raised, it will try to import it as
    a module."""
    pass


routines = LabeledRegistry()


class Connector(object):
    """"The connector for sequences of routines.
    Attaches to the acting routine, and references another routine by label.
    If the label is not in the registry, see if we can import it as a filename.
    """

    def __init__(self, source, source_modifiers):
        self.source_label = source
        self.source_modifiers = source_modifiers

    @classmethod
    def register(cls, label, routine):
        if label in routines:
            raise KeyError('Routine label conflict for {}.'.format(label))
        routines[label] = routine

    def get(self):
        # handle merges and all that...
        try:
            source_routine = routines[self.source_label]
        except KeyError:
            raise KeyError('The routine "{}" is not registered and could not'
                'be imported. Registered routines: {}'.format(self.source_label,
                ', '.join(routines.keys())))
        source_data = source_routine.get_all()
        return source_data



class FileSource(object):
    def __init__(self, filename):
        self.filename = filename

    def get(self):
        return open(self.filename, 'r')
            

class FileReadBase(RoutineBase):
    """Special class opens files.
    Does not connect to a source with a DataConnector.
    """
    __metaclass__ = ABCMeta

    def __init__(self, label, data_from):
        DataConnector.register(label, self)
        self._data_source = FileSource(data_from)

    def get_new(self, **kwargs):
        raise NotImplemented

    def get_all(self, **kwargs):
        return self.operate(**kwargs)

    def get_if(self, **kwargs):
        raise NotImplemented


class CSVImport(FileReadBase):
    """This import class expects a file-like stream as its source"""
    def __init__(self, map=None, const=None, **kwargs):
        super(CSVImport, self).__init__(**kwargs)
        self._map = map
        self.const = const

    def operate(self):
        from numpy import genfromtxt
        csv_config = {
            'delimiter': ',',
            'names': True,
            'dtype': None,
        }
        return genfromtxt(self.data, **csv_config)


class FileSaveBase(RoutineBase):

    def __init__(self, label, data_from, save_to, source_modifiers=None):
        self._data_source = DataConnector(data_from, source_modifiers)
        self.filename = save_to

