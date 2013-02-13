"""
do stuff with data
"""

import re
import logging
import pandas as pd


MODULE_RE = re.compile(r'(.*)\.(\w+)$')
CSV_RE = re.compile(r'.*\.csv$')


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

        raise KeyError('Can not find routine "{}".'.format(item))


routines = LabeledRegistry()


class Connector(object):
    """"The connector for sequences of routines.
    Attaches to the acting routine, and references another routine by label.
    If the label is not in the registry, see if we can import it as a filename.
    """

    @classmethod
    def register(cls, label, routine):
        if label in routines:
            raise KeyError('Routine label conflict for {}.'.format(label))
        routines[label] = routine

    def __init__(self, source, **modifiers):
        self.source_label = source
        self.source_modifiers = modifiers

    def get_from_source(self, source_label, **kwargs):
        # is it registered?
        source_routine = routines[self.source_label]
        if isinstance(source_routine, file):
            if re.match(CSV_RE, self.source_label):
                index_col = kwargs.get('index_col', 0)
                return pd.read_csv(source_routine, index_col=index_col)
            else:
                raise IOError('can\'t import that.')
        return source_routine.operate()

    def get(self, **kwargs):
        data = self.get_from_source(self.source_label, **kwargs)

        if self.source_modifiers.get('filter'):
            logging.debug('getting from' + self.source_label +
                'and filtering' + self.source_modifiers.get('filter'))
            try:
                data = data[data == True]
            except KeyError:
                try:
                    data = data[data[
                        self.source_modifiers.get('filter') == 'true']]
                except:
                    raise

        if self.source_modifiers.get('merge'):
            raise NotImplementedError

        logging.debug('connector.get from' + self.source_label + 'finishing')
        if not isinstance(data, pd.DataFrame):
            logging.debug('not dataframe, converting')
            data = pd.DataFrame(data)
        return data

    def __repr__(self):
        return '<Connector from {self.source_label}>'.format(self=self)


class FileSource(object):
    def __init__(self, filename):
        self.filename = filename

    def get(self):
        return open(self.filename, 'r')
            
