#!/usr/bin/python
"""
run a timeflow thing
"""

from timeflow import LabeledRegistry, get_map


def setup(workflow_file):
    import yaml

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
    import argparse, logging

    parser = argparse.ArgumentParser(description="TimeFlow is a simple utility"\
        " for managing indexed data-processing workflows.",
        epilog="The goal is to make it painless (and even fun?) to write your"\
        " genius algorithms as stand-alone routiens, which you can plug"\
        " together using a declarative YAML workflow definition.")
    # positional arguments
    parser.add_argument('workflow', help='the yaml workflow description')

    # optional arguments
    parser.add_argument('--version', action='store_false',
                        help='report the version of the timeflow installation')
    loudness = parser.add_mutually_exclusive_group()
    loudness.add_argument('-v', '--verbose', action='store_true',
                        help='show lots of running info')
    loudness.add_argument('-q', '--quiet', action='store_true',
                        help='mute console output')

    # control arguments
    control = parser.add_argument_group('control arguments')
    control.add_argument('-r', '--routine', default='save',
                         help='the routine whose output you want')
    control.add_argument('-c', '--column', dest='column', nargs='+',
                         help='retrieve specified columns')
    control.add_argument('-f', '--filter', dest='filtercolumn',
                         help='remove rows where this column evaluats false')

    # output arguments
    out = parser.add_argument_group('output options')
    out.add_argument('-o', '--output', default='timeflowed',
                     help='filename to save')
    out.add_argument('-t', '--type', dest='outputtype', default='csv',
                     choices=['csv', 'plot'],
                     help='type to output')

    args = parser.parse_args()

    if not args.quiet:
        logging.basicConfig(filename='timeflow_run.log', level=logging.INFO)
        logging.info('setting up logging...')

    workflow_file = open(args.workflow, 'r')
    registry = setup(workflow_file)

    print getattr(registry[args.routine], get_map[args.get])()
