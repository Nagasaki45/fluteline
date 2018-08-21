'''
Easy thread based pipelines.
'''

import threading

try:
    import queue  # python 3
except ImportError:
    import Queue as queue


class _TerminationMessage(object):
    '''
    Send me to a node input to stop it.
    '''
    pass


class Node(threading.Thread):
    '''
    A node is either a consumer or producer in a pipeline.

    ## Hooks

    Inherit and override `generate` to create a producer and `consume`
    to create a consumer or consumer-producer. Setup resources when
    starting in `enter` and clean after yourself in `exit`.

    ## Outputting values

    Your `generate` or `consume` functions can output values with
    `self.put(new_value)`.

    ## Connect, start, and stop

    First, connect the node to a destination with `connect(other_node)`,
    then call `start`. Call `stop` when you want to finish.

    ## Notes

    See also the utility functions `connect`, `start`, and `stop` to
    manage complete pipelines.
    '''
    def __init__(self):
        super(Node, self).__init__()
        self._input = queue.Queue()
        self._output = queue.Queue()  # In case nothing is connected

    def generate(self):
        '''
        Override to create producers.
        '''
        pass

    def consume(self, item):
        '''
        Override to create a consumer or consumer-producer.
        '''
        pass

    def enter(self):
        '''
        Override to prepare resources.
        '''
        pass

    def exit(self):
        '''
        Override to cleanup after yourself.
        '''
        pass

    def connect(self, other_node):
        '''
        Connect the output of this node to `other_node`'s input
        '''
        self._output = other_node._input

    def put(self, item):
        '''
        Output and item.
        '''
        self._output.put(item)

    def stop(self):
        '''
        Stop the node gracefully.
        '''
        self._input.put(_TerminationMessage)

    def run(self):
        self.enter()
        try:
            while True:
                if not self._input.empty():
                    item = self._input.get()
                    if item is _TerminationMessage:
                        break
                    self.consume(item)
                    self._input.task_done()
                self.generate()
        finally:
            self.exit()


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
