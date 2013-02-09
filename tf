#!/usr/bin/python
"""
run a timeflow thing
"""

import yaml
from timeflow import LabeledRegistry


routine_registry = LabeledRegistry()


def setup(workflow_file):
    workflow = yaml.load(workflow_file)
    map(build_routine, workflow.items())


def build_routine(routine_structure):
    label, config = routine_structure
    routine_label = config.pop('routine')
    routine = routine_registry[routine_label]
    routine_registry[label] = routine(label, **config)


def get(routine_name):
    return routine_registry[routine_name].get_all()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="timeflow",
                                     epilog="yep, timeflow")
    parser.add_argument('workflow', help='the yaml workflow description')
    parser.add_argument('-r', '--routine', default='save',
                        help='the routine whose output you want')
    args = parser.parse_args()

    setup(open(args.workflow, 'r'))
    print routine_registry[args.routine].get_all()
