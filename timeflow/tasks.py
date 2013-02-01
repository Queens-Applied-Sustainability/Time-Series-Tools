from abc import ABCMeta


class TaskBase(object):
    """Base class for tasks"""
    __metaclass__ = ABCMeta

    def __init__(self, arg):
        self.arg = arg




