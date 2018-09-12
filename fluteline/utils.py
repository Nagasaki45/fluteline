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
