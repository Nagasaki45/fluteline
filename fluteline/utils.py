from . import nodes
from . import queues


def connect(nodes):
    '''
    Connect a list of nodes.

    Connected nodes have an ``output`` member which is the following node in
    the line. The last node's ``output`` is a :class:`Queue` for
    easy plumbing.
    '''
    for a, b in zip(nodes[:-1], nodes[1:]):
        a.output = b
    b.output = queues.Queue()


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
