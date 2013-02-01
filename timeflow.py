import yaml


DEFAULT_WORKFLOW_FILENAME = 'workflow.yaml'


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
        try:
            workflow_file = open(workflow_file_name)
        except IOError:
            raise IOError("Couldn't open {}.".format(workflow_file_name))

    except IndexError:
        try:
            workflow_file = open(DEFAULT_WORKFLOW_FILENAME)
        except IOError:
            raise IOError("Couldn't find {}.".format(DEFAULT_WORKFLOW_FILENAME))


    workflow = yaml.load(workflow_file)

    print flowback(workflow, 'select')


