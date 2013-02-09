#!/usr/bin/python
"""
run a timeflow thing
"""

import yaml
from timeflow import LabeledRegistry


def setup(workflow_file):
    routine_registry = LabeledRegistry()
    workflow = yaml.load(workflow_file)
    
    def build_routine(routine_structure):
        label, config = routine_structure
        routine_label = config.pop('routine')
        routine = routine_registry[routine_label]
        routine_registry[label] = routine(label, **config)
    
    map(build_routine, workflow.items())

    return routine_registry


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="timeflow",
                                     epilog="yep, timeflow")
    parser.add_argument('workflow', help='the yaml workflow description')
    parser.add_argument('-r', '--routine', default='save',# nargs='+',
                        help='the routine whose output you want')
    parser.add_argument('-g', '--get', default='all', choices=['if', 'new', 'all'],
                        help='output mode for the routine')
    args = parser.parse_args()

    workflow_file = open(args.workflow, 'r')
    registry = setup(workflow_file)

    get_map = {'if': 'get_if', 'new': 'get_new', 'all': 'get_all'}
    print getattr(registry[args.routine], get_map[args.get])()
