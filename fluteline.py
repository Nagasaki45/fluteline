import abc
import logging
import threading
import warnings

try:
    import queue  # python 3
except ImportError:
    import Queue as queue


class _TerminationMessage(object):
    '''
    Send an instance to a node input to stop it.
    '''
    pass


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
        self.input = Queue()
        self.output = Queue()  # In case nothing is connected
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
        self.output = other_node.input

    def put(self, msg):
        '''
        Send a message to the next node in the pipeline.
        '''
        self.output.put(msg)

    def stop(self):
        '''
        Stop the node gracefully.
        '''
        self.input.put(_TerminationMessage())

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
        msg = self.input.get()
        if isinstance(msg, _TerminationMessage):
            self._stopping = True
        else:
            self.consume(msg)


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
        if self.input.empty():
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


class Logger(Consumer):
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


class Queue(object):
    '''
    Thread-safe input and output queue from nodes.
    '''
    def __init__(self):
        self._queue = queue.Queue()

    def empty(self):
        '''
        Return ``True`` if the queue is empty, ``False`` otherwise
        (not reliable!).
        '''
        return self._queue.empty()

    def put(self, item):
        '''
        Put an item into the queue.
        '''
        return self._queue.put(item)

    def get(self):
        '''
        Remove and return an item from the queue.
        '''
        return self._queue.get()
