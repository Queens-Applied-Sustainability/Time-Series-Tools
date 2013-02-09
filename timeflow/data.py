"""
do stuff with data
"""

import re
import pandas as pd


CSV_RE = re.compile(r'.*\.csv$')


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

    def get(self, **kwargs):
        # handle merges and all that...
        try:
            # is it registered?
            source_routine = routines[self.source_label]
            return source_routine.get_all()
        except KeyError:
            # can we open it as a file?
            try:
                data_file = open(self.source_label, 'r')
            except IOError:
                # TODO: try to import a module...
                raise KeyError('The routine "{}" is not registered and could '
                               ' not be opened or imported. Registered '
                               'routines: {}'.format(self.source_label,
                               ', '.join(routines.keys())))
            finally:
                if re.match(CSV_RE, self.source_label):
                    index_col = kwargs.get('index_col', 0)
                    source_data = pd.read_csv(data_file,
                                              index_col=index_col)
                    return source_data
        raise KeyError('Could not get {}.'.format(self.source_label))


class FileSource(object):
    def __init__(self, filename):
        self.filename = filename

    def get(self):
        return open(self.filename, 'r')
            
