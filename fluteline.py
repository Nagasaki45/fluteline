import abc
import threading
import warnings

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
    An abstract base class for producers, consumers, or consumer-producers
    in a pipeline.

    Hooks
        Setup resources when starting in ``enter`` and clean after yourself
        in ``exit``.

    Outputting values
        Send messages to the next node in the pipeline with
        ``self.put(new_value)``.

    Connect, start, and stop
        First, connect the node to a destination with ``connect(other_node)``,
        then call ``start``. Don't forget to call ``stop``. Otherwise the
        thread will stay alive.
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(Node, self).__init__()
        self._input = queue.Queue()
        self._output = queue.Queue()  # In case nothing is connected
        self._stopping = False

    def consume(self, msg):
        '''
        Override if your node should react to incoming message, whether it's
        a consumer, consumer-producer, or just a producer.

        :param msg: An incoming messages to process.
        '''
        warnings.warn('A message arrived to a node with no `consume` implementation')

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

    def put(self, msg):
        '''
        Send a message to the next node in the pipeline.
        '''
        self._output.put(msg)

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
            while not self._stopping:
                self._loop()
        finally:
            self.exit()

    @abc.abstractmethod
    def _loop(self):
        pass

    def _process_input(self):
        msg = self._input.get()
        if isinstance(msg, _TerminationMessage):
            self._stopping = True
            if msg.cascade == True:
                self.put(msg)
        else:
            self.consume(msg)
        self._input.task_done()


class Producer(Node):
    '''
    Inherit this class to create a producer.
    '''
    def produce(self):
        '''
        Override to produce new messages.
        '''
        pass

    def _loop(self):
        if self._input.empty():
            self.produce()
        else:
            self._process_input()



class Consumer(Node):
    '''
    Inherit this class to create a consumer or consumer-producer.
    '''
    def _loop(self):
        self._process_input()


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
