import threading

from . import queues


class _TerminationMessage(object):
    '''
    Send an instance to a node input to stop it.
    '''
    pass


class _Threaded(threading.Thread):
    def __init__(self):
        super(_Threaded, self).__init__()
        self._stopping = False

    def run(self):
        self.enter()
        try:
            while not self._stopping:
                self._loop()
        finally:
            self.exit()

    def _loop(self):
        pass

    def stop(self):
        self._stopping = True


class Node(object):
    '''
    A common interface for all fluteline nodes to start and stop them
    gracefully.

    Call ``start`` and ``stop`` to interact with the node. Override
    ``enter`` to setup resources and ``exit`` to clean after yourself.
    '''
    def start(self):
        '''
        Start the node.
        '''
        pass

    def stop(self):
        '''
        Stop the node gracefully.
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


class Producer(_Threaded, Node):
    '''
    Inherit this class to create producers.
    '''
    def produce(self):
        '''
        Override to produce new messages.
        '''
        pass

    def _loop(self):
        self.produce()


class Consumer(_Threaded, Node):
    '''
    Inherit this class to create consumers or consumer-producers.

    :var input: An input queue to accept messages.
    :vartype input: Queue
    '''
    def __init__(self):
        super(Consumer, self).__init__()
        self.input = queues.Queue()

    def consume(self, msg):
        '''
        Override to consume messages.
        '''
        pass

    def put(self, msg):
        '''
        Send a message to this consumer.
        '''
        self.input.put(msg)

    def stop(self):
        self.put(_TerminationMessage())

    def _loop(self):
        msg = self.input.get()
        if isinstance(msg, _TerminationMessage):
            self._stopping = True
        else:
            self.consume(msg)


class SynchronousConsumer(Node):
    '''
    Same API as :class:`Consumer` but... synchronous!

    - Execution happen the in thread that calls the ``put`` method.
    - ``enter`` and ``exit`` are called when calling ``start`` and ``stop``.
    - There's no input queue.
    - It's lighter on resources and usually faster.
    '''
    def start(self):
        self.enter()

    def stop(self):
        self.exit()

    def consume(self, msg):
        pass

    def put(self, msg):
        self.consume(msg)
