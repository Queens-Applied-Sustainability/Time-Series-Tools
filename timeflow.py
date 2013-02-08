#!/usr/bin/python

"""
$ timeflow workflow.yaml --routine select

ask registry for output from select
    not found, so load it
        check for dot in name...
        not found, so look in workflow for name... found.
    ask select for output
        select asks registry for output from import
            not found, so load it...
            ...
            import returns
        select applies processing to data
        select returns processed data

"""

import yaml
import timeflow


def build_routine(config):
    """instantiates the configured routine"""
    print 'Building {} routine...'.format(config['routine'])
    # try to import the class
    routine_name = config['routine']
    if '.' not in routine_name:
        raise KeyError('no routine "{}"'.format(routine_name))
    mod_parts = routine_name.split('.')
    module = __import__('.'.join(mod_parts[:-1]))
    routine_class = getattr(module, mod_parts[-1])
    init_config = dict((k, v) for k, v in config.items() if k != 'routine')
    routine = routine_class(**init_config)
    return routine


class Flow(object):
    """workflow registry"""
    def __init__(self, routine_config):
        self.routine_config = routine_config
        # set up the routine registry
        self.registry = {}

    def get(self, routine_label, **kwargs):
        """return the result of a routine"""
        try:
            # be optimistic
            routine = self.registry[routine_label]
        except KeyError:
            # see if it's in the standard config...
            try:
                config = self.routine_config[routine_label]
                routine = build_routine(config)
            except KeyError:
                # can we import it?
                if '.' not in routine_label:
                    raise KeyError('no routine "{}"'.format(routine_label))
                mod_parts = routine_label.split('.')
                module = __import__('.'.join(mod_parts[:-1]))
                routine = getattr(module, mod_parts[-1])

            self.registry[routine_label] = routine

        return routine.get(**kwargs)




        


def flowback(workflow, label):
    """build working stuff"""
    step_meta = workflow[label]

    if step_meta['data']['from'] in workflow.keys():
        data_from = flowback(workflow, step_meta['data']['from'])
    elif '.' not in step_meta['data']['from']:
        raise ValueError('could not find step {}'.format(step_meta['data']['from']))
    else:
        data_parts = step_meta['data']['from'].split('.')
        data_module = __import__('.'.join(data_parts[:-1]))
        data_step = getattr(data_module, data_parts[-1])
        data_from = data_step(**step_meta['data'])

    routine_parts = step_meta['routine'].split('.')
    module_name = '.'.join(routine_parts[:-1])
    routine_name = routine_parts[-1]
    module = __import__(module_name)
    routine = getattr(module, routine_name)

    step = routine(step_meta, data_from=data_from)
    return step


if __name__ == '__main__':
    import os, sys
    try:
        workflow_file_name = sys.argv[1]
    except IndexError:
        raise LookupError('missing input filename')
    try:
        routine_name = sys.argv[2]
    except IndexError:
        raise LookupError('missing routine name')

    try:
        workflow_file = open(workflow_file_name)
    except IOError:
        raise LookupError('could not open {}'.format(workflow_file_name))

    workflow = yaml.load(workflow_file)

    flow = Flow(workflow)

    print flow.get(routine_name)


