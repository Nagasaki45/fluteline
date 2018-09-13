import abc
import threading
import warnings

from . import queue


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

    Start and stop
        Call ``start`` to spin up the node. Don't forget to call ``stop``.
        Otherwise the thread will stay alive.
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(Node, self).__init__()
        self.input = queue.Queue()
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

    def put(self, msg):
        '''
        Send a message to this node.
        '''
        self.input.put(msg)

    def stop(self):
        '''
        Stop the node gracefully.
        '''
        self.put(_TerminationMessage())

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
