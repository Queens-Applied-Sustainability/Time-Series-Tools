"""
do stuff with data
"""

import re
import pandas as pd


MODULE_RE = re.compile(r'(.*)\.(\w+)$')
CSV_RE = re.compile(r'.*\.csv$')


get_map = {
    'if_true': 'get_if_true',
    'if_false': 'get_if_false',
    'new': 'get_new',
    'all': 'get_all',
}


class LabeledRegistry(dict):
    """like a dict, but if a keyerror is raised, it will try to import it as
    a module."""
    def __getitem__(self, item):
        try:
            # first try to return from the registry
            return super(LabeledRegistry, self).__getitem__(item)
        except KeyError: pass

        try:
            # ok, try importing a module
            mod, cls = re.match(MODULE_RE, item).groups()
            mod = __import__(mod)
            return getattr(mod, cls)
        except (ImportError, AttributeError): pass

        try:
            # fine. open a file?
            return open(item, 'r')
        except IOError: pass

        raise KeyError('can not get "{}".'.format(item))


routines = LabeledRegistry()


class Connector(object):
    """"The connector for sequences of routines.
    Attaches to the acting routine, and references another routine by label.
    If the label is not in the registry, see if we can import it as a filename.
    """

    def __init__(self, source, **modifiers):
        self.source_label = source
        self.source_modifiers = modifiers

    @classmethod
    def register(cls, label, routine):
        if label in routines:
            raise KeyError('Routine label conflict for {}.'.format(label))
        routines[label] = routine

    def get(self, **kwargs):
        # handle merges and all that...

        # is it registered?
        source_routine = routines[self.source_label]
        if isinstance(source_routine, file):
            if re.match(CSV_RE, self.source_label):
                index_col = kwargs.get('index_col', 0)
                return pd.read_csv(source_routine, index_col=index_col)
            else:
                raise IOError('can\'t import that.')

        get = kwargs.get('get', 'all')
        return getattr(source_routine, get_map[get])()


class FileSource(object):
    def __init__(self, filename):
        self.filename = filename

    def get(self):
        return open(self.filename, 'r')
            
