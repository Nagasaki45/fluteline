import threading

try:
    import queue  # python 3
except ImportError:
    import Queue as queue


class _TerminationMessage(object):
    '''
    Send an instance to a node input to stop it. A cascading
    termination message will stream through the pipeline to the
    following nodes.
    '''
    def __init__(self, cascade):
        self.cascade = cascade


class Node(threading.Thread):
    '''
    A node is either a producer, consumer or consumer-producer in a pipeline.

    Hooks
        Inherit and override ``generate`` to create a producer and ``consume``
        to create a consumer or consumer-producer. Setup resources when
        starting in ``enter`` and clean after yourself in ``exit``.

    Outputting values
        Your ``generate`` or ``consume`` functions can output values with
        ``self.put(new_value)``.

    Connect, start, and stop
        First, connect the node to a destination with ``connect(other_node)``,
        then call ``start``. Don't forget to call ``stop``. Otherwise the
        thread will stay alive.

    Notes
        Use the utility functions ``connect``, ``start``, and ``stop`` to
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
        Connect the output of this node to ``other_node``'s input.
        '''
        self._output = other_node._input

    def put(self, item):
        '''
        Output and item.
        '''
        self._output.put(item)

    def stop(self, cascade=False):
        '''
        Stop the node gracefully.

        :param bool cascade: Cascade the stopping message to the following
            nodes.
        '''
        self._input.put(_TerminationMessage(cascade))

    def run(self):
        self.enter()
        try:
            while True:
                if not self._input.empty():
                    item = self._input.get()
                    if isinstance(item, _TerminationMessage):
                        if item.cascade == True:
                            self.put(item)
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
