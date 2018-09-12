import logging

from . import nodes


def connect(nodes):
    '''
    Connect a list of nodes.
    '''
    for a, b in zip(nodes[:-1], nodes[1:]):
        a.connect(b)


def start(nodes):
    '''
    Start multiple nodes.
    '''
    for node in nodes:
        node.start()


def stop(nodes):
    '''
    Stop multiple nodes.
    '''
    for node in nodes:
        node.stop()


class Logger(nodes.Consumer):
    '''
    A utility consumer-producer that logs messages.
    '''
    def __init__(self, logger=None):
        '''
        :param logger: Provide your own logger or get a new
                       ``fluteline`` logger. Logging level is
                       ``logging.INFO``.
        '''
        super(Logger, self).__init__()
        if logger is None:
            logger = logging.getLogger(__name__)
        self.logger = logger


    def consume(self, msg):
        self.logger.info(msg)
        self.put(msg)
