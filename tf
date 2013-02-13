#!/usr/bin/python
"""
Parse a declarative workflow configuration and run it.
"""

def setup(workflow_file):
    import yaml
    from timeflow import LabeledRegistry

    routine_registry = LabeledRegistry()

    logging.debug('loading yaml workflow')
    workflow = yaml.load(workflow_file)
    if not isinstance(workflow, dict):
        raise ValueError('Workflow "{}" did not parse to a dict (is it yaml?)'
            .format(workflow_file.name))
    
    def build_routine(routine_structure):
        label, config = routine_structure
        routine_label = config.pop('routine')
        routine = routine_registry[routine_label]
        routine_registry[label] = routine(label, **config)
    
    map(build_routine, workflow.items())

    return routine_registry


def get_connected(source, filtercolumn):
    from timeflow import Connector

    if filtercolumn and '=' in filtercolumn:
        raise NotImplemented

    data = Connector(source, filter=filtercolumn)
    return data


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
                        help='suppress info and warnings')

    # control arguments
    control = parser.add_argument_group('control arguments')
    control.add_argument('-r', '--routine', default='save',
                         help='the routine whose output you want')
    # control.add_argument('-c', '--column', dest='column', nargs='+',
    #                      help='retrieve specified columns')
    control.add_argument('-f', '--filter', dest='filtercolumn',
                         help='remove rows where this column evaluates false')

    # output arguments
    out = parser.add_argument_group('output options')
    out.add_argument('-o', '--output', default='timeflowed',
                     help='filename to save')
    out.add_argument('-t', '--type', dest='outputtype', default='csv',
                     choices=['csv', 'plot'],
                     help='type to output')

    args = parser.parse_args()

    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    elif not args.verbose:
        logging.basicConfig(level=logging.INFO)
    elif args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug('opening workflow file')
    workflow_file = open(args.workflow, 'r')

    logging.debug('registering workflow routines')
    registry = setup(workflow_file)

    logging.debug('connecting to routine "{}"'.format(args.routine))
    data = get_connected(args.routine, args.filtercolumn)

    print data.get()
    # logging.info('Running workflow for "{}"...'.format(args.routine))

